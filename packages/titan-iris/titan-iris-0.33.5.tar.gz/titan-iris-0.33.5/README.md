# TitanML iris package

## 🎯 About

Iris is your portal to the TitanML platform.
Using Iris, you can setup Takeoff servers, launch jobs to run on TitanML servers, run your own models and datasets through our compression algorithms, and explore and download the optimised models from the Titan Store.

For usage information, tutorials, and usage examples, see the [docs](https://docs.titanml.co/docs/intro).

<h1 align="center">New! Try the TitanML Takeoff Server</h1>

<p align="center">
  <img src="https://github.com/titanml/takeoff/assets/6034059/5b561d1a-7be3-4258-bd4d-bb670fdb2c1e" alt="Image from TitanML">
</p>

✔️ Easy deployment and streaming responses for popular Large Language Models

✔️ Optimized int8 quantization

✔️ Chat and playground-like interface

✔️ Support for encoder-decoder (T5 family) and decoder models

For the pro edition, including multi-gpu inference, int4 quantization, and more [contact us](mailto:hello@titanml.co)

## Dependencies

Iris is tested on the following versions of python:

- python >= 3.7 <=3.10

Iris should work on later versions, but likely won't work on earlier versions.

## iris API

**Usage**:

<pre class="language-console"><code class="lang-console"><strong>$ iris [OPTIONS] COMMAND [ARGS]...
</strong></code></pre>

**Options**:

- `--help`: Show this message and exit.

**Commands**:

- `delete`: delete objects from the TYTN api.
- `download`: Download the titan-optimized onnx model.
- `get`: Get objects from the TYTN api.
- `infer`: Run inference on a model.
- `login`: Login to iris.
- `logout`: Logout from iris.
- `makesafe`: Convert a non-safetensor model into a...
- `post`: Dispatch a job to the TitanML platform
- `pull`: Pull the titan-optimized server docker image.
- `status`: Get the status of an experiment
- `upload`: Upload an artefact to the TitanML hub.
- `takeoff`: Launch a TitanML inference server. See [docs](https://docs.titanml.co/docs/titan-takeoff/getting-started) for more information.

## Help

For more information on the Iris CLI, see the [docs](https://docs.titanml.co/).

## Authors

TitanML
