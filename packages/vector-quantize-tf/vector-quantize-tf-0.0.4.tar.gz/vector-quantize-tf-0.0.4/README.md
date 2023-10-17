# vector-quantize-tf

[![PyPI](https://img.shields.io/pypi/v/vector-quantize-tf.svg)](https://pypi.org/project/vector-quantize-tf)

残差ベクトル量子化の tensorflow の実装

# インストール

```
pip install vector-quantize-tf
```

# 使い方

```py
from vector_quantize_tf import ResidualVQ

residual_vq = ResidualVQ(
    input_dim=252, # このレイヤーに入力するテンソルの特徴次元
    codebook_size=1024,
    embedding_dim=32,
    num_quantizers=8,
    batch_size=8,
    ema_decay=0.99,
    threshold_ema_dead_code=0.,
    commitment_cost=1.0,
)
inputs = tf.random.uniform([2, 10, 252])
quantized, indices = residual_vq(inputs)
```

K-Means を使って初期化する場合以下のように`kmeans_init`を True にします。

```py
from vector_quantize_tf import ResidualVQ

residual_vq = ResidualVQ(
    input_dim=252, # このレイヤーに入力するテンソルの特徴次元
    codebook_size=1024,
    embedding_dim=32,
    num_quantizers=8,
    batch_size=8,
    ema_decay=0.99,
    threshold_ema_dead_code=2,
    kmeans_init=True
)
inputs = tf.random.uniform([2, 10, 252])
quantized, indices = residual_vq(inputs)
```
