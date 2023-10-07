A package designed to generate the Meilisearch API key and implement it in config.yml meilisync service

This package will be useful for those who use the docker meilisync image in their project and need to generate an injected key at the time the container is launched.

To generate a key, in the system where the script will be launched, the key must be specified as an environment variable called MEILI_MASTER_KEY

This package runs from the command line and allows you to use the following parameters:

--path (def. ./config.example.yml) - Used to specify an example configuration file.
--output (def. ./config.yml) - Used to specify the path where the configuration file will be located
--address (def. http://localhost:7700) - Meilisearch service address