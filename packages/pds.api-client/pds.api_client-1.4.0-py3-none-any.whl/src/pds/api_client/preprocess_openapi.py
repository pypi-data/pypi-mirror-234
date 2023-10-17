import yaml
import argparse
import tempfile
import shutil
import subprocess


def preprocess(input: dict):

    new_tags_dict = {t['name']: t['name'][3:] for t in input['tags']}
    for path in input['paths'].keys():
        tags = input['paths'][path]['get']['tags']
        new_tags = [new_tags_dict.get(tag, tag) for tag in tags]
        input['paths'][path]['get']['tags'] = new_tags

    # remove the * object which is confusing for the api generator
    for k, r in input['components']['responses'].items():
        del r['content']['*']

    return input


def run_openapi_gen(input, version):
    with tempfile.NamedTemporaryFile(mode='w', delete=True) as file:
        yaml.dump(input, file)
        shutil.rmtree('pds', ignore_errors=True)
        shutil.rmtree('test', ignore_errors=True)

        # to test with the latest version of the openapi-generator
        # openapi_generator_cmd = [
        #    'java',
        #    '-jar',
        #    '.../openapi-generator/modules/openapi-generator-cli/target/openapi-generator-cli.jar'
        #    ]

        openapi_generator_cmd = ['openapi-generator']
        openapi_generator_cmd.extend([
            'generate',
            '--skip-validate-spec',
            '-g',
            'python-nextgen',
            '-i',
            file.name,
            '--package-name',
            'pds.api_client',
            f'--additional-properties=packageVersion={version}'
        ])
        subprocess.run(openapi_generator_cmd)


def main():

    parser = argparse.ArgumentParser(
                    prog='Process yaml openapi',
                    description='Remove features unsupported by openapi-generator, python-nextgen language',
    )
    parser.add_argument('input_yaml')
    parser.add_argument('-v', '--version', help="version of the package to be generated")

    args = parser.parse_args()

    with open(args.input_yaml, "r") as stream:
        try:
            input = yaml.safe_load(stream)
            preprocess(input)
            run_openapi_gen(input, args.version)
            shutil.copy('.gitignore-orig', '.gitignore')
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':
    main()