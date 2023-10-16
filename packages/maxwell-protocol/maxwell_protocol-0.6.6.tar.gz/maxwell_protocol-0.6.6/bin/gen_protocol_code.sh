#!/bin/bash

current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )";
cd ${current_dir}

# Fetch proto files
if [[ ! -d proto ]]; then
    git clone -b main https://github.com/maxwell-dev/maxwell-protocol.git proto;
fi

# Init packages
mkdir -p maxwell/protocol
touch maxwell/__init__.py
touch maxwell/protocol/__init__.py

echo "try:
  __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
  __path__ = __import__('pkgutil').extend_path(__path__, __name__)
" > maxwell/__init__.py

# Generate pb files
protoc -I=proto --python_out=maxwell/protocol maxwell_protocol.proto

# Generate api files
bin/gen_protocol_api.py \
    --proto_file proto/maxwell_protocol.proto \
    --enum_type_names msg_type_t
