from amazon_emr_serverless_image_cli.commands.validate_image import ValidateImage
from amazon_emr_serverless_image_cli.helper import argument_parser, print_message
from amazon_emr_serverless_image_cli.helper.logging import Log


def run():
    args = argument_parser.parse_commandline_arguments()
    log = Log()
    print_message.print_pre_verification_text()

    if args.command is not None:
        commands = {"validate-image": ValidateImage()}

        commands[args.command].initiate(args, log)
        commands[args.command].run()
