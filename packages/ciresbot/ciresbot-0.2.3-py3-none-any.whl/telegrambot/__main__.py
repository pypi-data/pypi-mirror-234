from telegrambot.cli import create_parser
from telegrambot.utils import send_message, send_photo, get_updates


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.mode == "message":
        send_message(
            args.bot,
            args.token,
            args.bot_file,
            args.chat,
            args.id,
            args.chat_file,
            args.message
        )
    elif args.mode == "photo":
        send_photo(
            args.bot,
            args.token,
            args.bot_file,
            args.chat,
            args.id,
            args.chat_file,
            args.photo,
            args.caption,
        )
    elif args.mode == "updates":
        get_updates(
            args.bot,
            args.token,
            args.bot_file,
        )
    else:
        raise ValueError(f"Invalid mode {args.mode}")


if __name__ == "__main__":
    main()
