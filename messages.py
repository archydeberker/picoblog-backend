class Onboarding:
    need_name = """
                🙏 We need to know your name to complete your onboarding. Please send us your name with the hashtag #name, like '#name Joe Bloggs'
                """

    need_location = """
                🌍 Where in the world are you? Please send us your location with the hashtag #location" like '#location El Chalten, Patagonia'
               """

    onboarding_complete = [
        """
                Your onboarding is complete. You can now write blogposts. You can send messages and images, and when you're finished, send a message with #publish!
                """,
        """
                You can set the title of your blogpost with the tag #title, like '#title The day the teddy bears had their picnic'.
                """,
        """
                Now get out there and have some adventures worth writing about 🧗⛷🚴🗺‍‍
                """,
    ]

    @staticmethod
    def welcome(user):

        return f"Welcome, {user.name} from {user.location} 🚀. Your picoblog is being " \
               f"built at https://http://picoblog.netlify.app/blog/{user.slug} 🛠"