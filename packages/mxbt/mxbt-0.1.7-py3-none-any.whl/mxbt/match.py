class Match:
    """
    Class with methods to filter events

    ...

    """

    def __init__(self, room, event, bot) -> None:
        """
        Initializes the simplematrixbotlib.Match class.

        ...

        Parameters
        ----------
        room : nio.rooms.MatrixRoom
            The bot developer will use the room parameter of the handler function for this.
    
        event : nio.events.room_events.Event
            The bot developer will use the event parameter of the handler function for this.
        
        bot : simplematrixbotlib.Bot
            The bot developer will use the bot's instance of the simplematrixbotlib.Bot class for this.

        """
        self.room = room
        self.event = event
        self._bot = bot

    def is_from_userid(self, userid):
        """
        Parameters
        ----------
        userid : str
            The userid of a user.

        Returns
        -------
        boolean
            Returns True if the event was sent from the specified userid
        """
        return self.event.sender == userid

    def is_from_allowed_user(self):
        """
        Returns
        -------
        boolean
            Returns True if the event was sent from an allowed userid
        """
        allowlist = self._bot.config.allowlist
        blocklist = self._bot.config.blocklist
        sender = self.event.sender
        # if there is no explicit allowlist, default to allow
        is_allowed = False if len(allowlist) > 0 else True

        for regex in allowlist:
            if regex.fullmatch(sender):
                is_allowed = True
                break

        for regex in blocklist:
            if regex.fullmatch(sender):
                is_allowed = False
                break

        return is_allowed

    def is_from_self(self):
        """
        
        Returns
        -------
        boolean
            Returns True if the event is from a user that is not this bot.
        """
        return self.is_from_userid(self._bot.async_client.user_id)


    @staticmethod
    def is_from_users(sender: str, users: list) -> bool:
        """
        Returns 
        -------
        boolean
            Returns True if the sender in users list 
        """
        return sender in users

    @staticmethod
    def is_from_rooms(room_id: str, rooms: list) -> bool:
        """
        Returns 
        -------
        boolean
            Returns True if the room_id in rooms list 
        """
        return room_id in rooms

