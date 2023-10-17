import tensorflow as tf
from sklearn.cluster import KMeans


class GumbelSoftmaxLayer(tf.keras.layers.Layer):
    def __init__(
            self,
            initial_temperature=2.0,
            anneal_factor=0.999995,
            min_temperature=0.5,
            **kwargs):
        super(GumbelSoftmaxLayer, self).__init__(**kwargs)
        self.initial_temperature = initial_temperature
        self.use_temperature = self.initial_temperature != 0.0
        self.anneal_factor = anneal_factor
        self.min_temperature = min_temperature

    def build(self, input_shape):
        self.temperature = tf.Variable(
            self.initial_temperature,
            dtype=tf.float32,
            trainable=False,
            name="temperature")

    def call(self, inputs, training=False):
        if not self.use_temperature or not training:
            indices = tf.argmax(inputs, axis=1)
            encodings = tf.one_hot(indices, tf.shape(inputs)[1])
            return indices, encodings

        gumbel_noise = tf.random.uniform(shape=tf.shape(
            inputs), minval=0, maxval=1, dtype=tf.float32)
        gumbel_noise = -tf.math.log(-tf.math.log(gumbel_noise))

        outputs = tf.argmax(
            tf.nn.softmax(
                (inputs + gumbel_noise) / self.temperature,
                axis=1),
            axis=1)
        encodings = tf.one_hot(outputs, tf.shape(inputs)[1])

        self.update_temperature()
        return outputs, encodings

    def update_temperature(self):
        if not self.use_temperature:
            return

        new_temperature = tf.maximum(
            self.temperature *
            self.anneal_factor,
            self.min_temperature)
        self.temperature.assign(new_temperature)

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "initial_temperature": self.initial_temperature,
                "anneal_factor": self.anneal_factor,
                "min_temperature": self.min_temperature
            }
        )
        return config


class VectorQuantizer(tf.keras.layers.Layer):
    """
    Args:
        embedding_dim: 埋め込み次元
        num_embeddings: コードブックのサイズ
    """

    def __init__(
            self,
            embedding_dim,
            codebook_size,
            batch_size,
            ema_decay,
            epsilon=1e-6,
            commitment_cost=1.0,
            threshold_ema_dead_code=2.0,
            sample_codebook_temperature=0.0,
            kmeans_init=False,
            **kwargs):
        super().__init__(**kwargs)
        self.embedding_dim = embedding_dim
        self.codebook_size = codebook_size
        self.batch_size = batch_size
        self.ema_decay = ema_decay
        self.epsilon = epsilon
        self.commitment_cost = commitment_cost
        self.threshold_ema_dead_code = threshold_ema_dead_code
        self.kmeans_init = kmeans_init

        self.gumbel_softmax = GumbelSoftmaxLayer(
            initial_temperature=sample_codebook_temperature,
            dtype=tf.float32)

    def build(self, input_shape):
        self.embeddings = self.add_weight(
            name="embeddings",
            shape=(self.embedding_dim, self.codebook_size),
            dtype=tf.float32,
            initializer=tf.keras.initializers.random_normal(),
            trainable=False)
        self.ema_cluster_size = self.add_weight(
            name="ema_cluster_size",
            shape=(self.codebook_size,),
            dtype=tf.float32,
            initializer='zeros',
            trainable=False)
        self.ema_w = self.add_weight(
            name="ema_w",
            shape=(self.embedding_dim, self.codebook_size),
            dtype=tf.float32,
            initializer=tf.initializers.Constant(self.embeddings.numpy()),
            trainable=False)

        self.initialized = tf.Variable(
            False,
            dtype=tf.bool,
            trainable=False,
            name="initialized")

    def init_embeddings(self, inputs):
        if self.initialized:
            return

        kmeans = KMeans(
            n_clusters=self.codebook_size,
            random_state=0).fit(inputs.numpy())

        embedding = tf.convert_to_tensor(
            kmeans.cluster_centers_.T, dtype=tf.float32)
        cluster_size = tf.math.bincount(
            tf.convert_to_tensor(
                kmeans.labels_,
                dtype=tf.int32),
            minlength=self.codebook_size)
        cluster_size = tf.cast(cluster_size, dtype=tf.float32)
        embedding_w = embedding * \
            tf.reshape(cluster_size, [1, -1])

        self.embeddings.assign(embedding)
        self.ema_w.assign(embedding_w)
        self.ema_cluster_size.assign(cluster_size)
        self.initialized.assign(True)

    def expire_codes(self, batch_samples):
        if self.threshold_ema_dead_code <= 0.0:
            return

        dead_codes = self.ema_cluster_size < self.threshold_ema_dead_code

        indices_to_update = tf.where(dead_codes)
        flat_samples = tf.reshape(batch_samples, [-1, tf.shape(batch_samples)[-1]])
        sample_indices = tf.random.shuffle(tf.range(tf.shape(flat_samples)[0]))[:self.codebook_size]
        sampled_vectors = tf.gather(flat_samples, sample_indices)
        vectors_to_update = tf.gather(sampled_vectors, tf.range(tf.minimum(tf.shape(indices_to_update)[0], tf.shape(sampled_vectors)[0])))
        
        updated_embeddings = tf.transpose(self.embeddings)
        updated_embeddings = tf.tensor_scatter_nd_update(updated_embeddings, indices_to_update, vectors_to_update)
        self.embeddings.assign(tf.transpose(updated_embeddings))

        updated_ema_cluster_size = tf.where(
            dead_codes,
            tf.ones_like(
                self.ema_cluster_size) *
            self.threshold_ema_dead_code,
            self.ema_cluster_size)
        self.ema_cluster_size.assign(updated_ema_cluster_size)

        updated_ema_w = tf.where(
            tf.expand_dims(dead_codes, axis=-1),
            updated_embeddings * self.threshold_ema_dead_code,
            tf.transpose(self.ema_w)
        )
        self.ema_w.assign(tf.transpose(updated_ema_w))

    def call(self, inputs, training=False):
        flat_inputs = tf.reshape(inputs, [-1, self.embedding_dim])

        if self.kmeans_init:
            tf.py_function(self.init_embeddings, inp=[flat_inputs], Tout=[])

        encoding_indices, encodings = self.get_code_indices(
            flat_inputs, training=training)
        encoding_indices = tf.reshape(encoding_indices, tf.shape(inputs)[:-1])
        quantized = tf.nn.embedding_lookup(
            tf.transpose(self.embeddings, [1, 0]),
            encoding_indices)

        if training:
            cluster_size = tf.reduce_sum(encodings, 0)
            updated_ema_cluster_size = tf.keras.backend.moving_average_update(
                self.ema_cluster_size, cluster_size, self.ema_decay)

            dw = tf.matmul(
                flat_inputs,
                encodings,
                transpose_a=True)
            updated_ema_w = tf.keras.backend.moving_average_update(
                self.ema_w, dw, self.ema_decay)

            n = tf.reduce_sum(updated_ema_cluster_size)
            updated_ema_cluster_size = (
                (updated_ema_cluster_size + self.epsilon) / (n + self.codebook_size * self.epsilon) * n)
            normalized_updated_ema_w = updated_ema_w / \
                tf.reshape(updated_ema_cluster_size, [1, -1])
            self.embeddings.assign(normalized_updated_ema_w)

            self.expire_codes(inputs)

        e_latent_loss = tf.reduce_mean(
            tf.square(tf.stop_gradient(quantized) - inputs))
        loss = e_latent_loss * self.commitment_cost
        if training:
            quantized = inputs + tf.stop_gradient(quantized - inputs)

        return {
            "quantized": quantized,
            "encodings": encodings,
            "encoding_indices": encoding_indices,
            "loss": loss
        }

    def get_code_indices(self, flat_inputs, training=False):
        similarity = tf.matmul(flat_inputs, self.embeddings)

        flat_inputs_sum = tf.reduce_sum(
            flat_inputs ** 2,
            axis=1,
            keepdims=True)
        embedding_sum = tf.reduce_sum(
            self.embeddings ** 2,
            axis=0,
            keepdims=True)

        distances = (flat_inputs_sum - 2 * similarity) + embedding_sum

        encoding_indices, encodings = self.gumbel_softmax(
            -distances, training=training)
        return encoding_indices, encodings

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "embedding_dim": self.embedding_dim,
                "codebook_size": self.codebook_size,
                "ema_decay": self.ema_decay,
                "epsilon": self.epsilon,
                "threshold_ema_dead_code": self.threshold_ema_dead_code,
                "kmeans_init": self.kmeans_init,
                "dead_code_warmup_steps": self.dead_code_warmup_steps
            }
        )
        return config


class ResidualVQ(tf.keras.layers.Layer):
    def __init__(
            self,
            input_dim,
            codebook_size,
            embedding_dim,
            num_quantizers,
            batch_size,
            ema_decay,
            threshold_ema_dead_code,
            commitment_cost=0.0,
            sample_codebook_temperature=0,
            kmeans_init=False,
            **kwargs):
        super().__init__(**kwargs)
        self.input_dim = input_dim
        self.codebook_size = codebook_size
        self.embedding_dim = embedding_dim
        self.num_quantizers = num_quantizers
        self.batch_size = batch_size
        self.commitment_cost = commitment_cost
        self.vq_layers = [
            VectorQuantizer(
                embedding_dim=embedding_dim,
                codebook_size=codebook_size,
                batch_size=batch_size,
                ema_decay=ema_decay,
                threshold_ema_dead_code=threshold_ema_dead_code,
                commitment_cost=commitment_cost,
                sample_codebook_temperature=sample_codebook_temperature,
                kmeans_init=kmeans_init,
                dtype=tf.float32)
            for _ in range(num_quantizers)]

        self.projection_in = tf.keras.layers.Dense(
            embedding_dim,
            dtype=tf.float32) if input_dim != embedding_dim else tf.keras.layers.Identity(
            dtype=tf.float32)
        self.projection_norm = tf.keras.layers.LayerNormalization(
            dtype=tf.float32) if input_dim != embedding_dim else tf.keras.layers.Identity(
            dtype=tf.float32)
        self.projection_out = tf.keras.layers.Dense(
            input_dim,
            dtype=tf.float32) if input_dim != embedding_dim else tf.keras.layers.Identity(
            dtype=tf.float32)

    def get_embeddings(self):
        return [layer.embeddings for layer in self.vq_layers]

    def call(self, inputs, training=False):
        inputs = self.projection_in(inputs)
        inputs = self.projection_norm(inputs)

        residual = inputs
        quantized_out = 0.

        losses = []
        encoding_indices = []
        for layer in self.vq_layers:
            vq_output = layer(residual, training=training)

            residual = residual - tf.stop_gradient(vq_output['quantized'])
            quantized_out = quantized_out + vq_output['quantized']

            losses.append(vq_output['loss'])
            encoding_indices.append(vq_output['encoding_indices'])

        if self.commitment_cost != 0:
            self.add_loss(tf.reduce_sum(losses))
            self.add_metric(
                tf.math.reduce_sum(losses),
                name="residual_vq_commitment")

        quantized_out = self.projection_out(quantized_out)

        return quantized_out, encoding_indices

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "codebook_size": self.codebook_size,
                "embedding_dim": self.embedding_dim,
                "num_quantizers": self.num_quantizers,
                "commitment_cost": self.commitment_cost
            }
        )
