<h1 align="center">
Confringo
</h1>

<h1>Contents</h1>

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->'

<!-- code_chunk_output -->

- [About](#about)
- [Run](#run)
- [Build](#build)
- [Usage](#usage)
  - [Configuration](#configuration)
  - [Injectors](#injectors)
  - [Resolvers](#resolvers)

<!-- /code_chunk_output -->


# About

Allow configuration to be injected to filesystem object from environment variables following a parse-resolve-inject workflow. The value this can provide is to help pre-configure other containers at run-time before they start through shared docker volumes.

# Run

```sh
docker pull kevindhira/confringo:0.1.0-experimental
```

# Build

```sh
pack build confringo --default-process confringo
```

# Usage


## Configuration

Parsing environment variables involves sorting and bucketing variables by prefix, and evaluating the appropriate injector to use.

For instance, see the following ENV variable declaration:

`<prefix>_<configuration_name>_TYPE=file`

eg:

`CFG_FOO_TYPE=file`

Where
- `<prefix>`: env variable prefix to consider (defaults to CFG_, overridable with `CONFRINGO_ENV_PREFIX` environment variable)
- `<configuration_name>`: name of the configuration
- `TYPE`: attribute to declare the (injector) type of the configuration

In this case, the `FOO` configuration specifies a `file` injector.

Other required attributes for a configuration can be set with:

`<prefix>_<configuration_name>_<attribute>=<value>`

eg:

`CFG_FOO_<attribute>=value`

Some attributes (currently `DATA` or `DATA_*`) get "resolved", as to allow transformations to the data via aggregators, fetchers, or encoders/decoders etc.

The syntax:

`CFG_FOO_DATA=[<resolverN>:<resolverN-1>:...]<resolver1>::<value>`

where multiple resolvers can be chained and operates on a RTL bases on the source `<value>`.

Eg consider:

`CFG_FOO_DATA=base64:ssm::/confringo/test`

will first look up the `/confringo/test` AWS SSM parameter store parameter, and immediately `base64` decode the returned value.

The docs (README or otherwise) will contain the required attributes for each of the injectors, as well as documentation on each of the resolvers.

## Injectors

List of Injectors
- File
- Paketo ca-certificates
- JKS Trustore
- PKCS12 Keystore

## Resolvers

List of Resolvers
- Base64 decoder
- TLS certificate fetcher via probe
- AWS SecretsManager Secret retrieve
- AWS SSM Parameter retrieve
