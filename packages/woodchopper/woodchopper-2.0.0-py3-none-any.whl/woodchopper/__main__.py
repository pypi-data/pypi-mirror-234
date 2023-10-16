from woodchopper import __version__, Logging_Levels, DateTime_Defaults, Styles, Logger

if __name__ == "__main__":
	log = Logger("monty.log", show_datetime=DateTime_Defaults.DATE_AND_TIME, logging_level=Logging_Levels.DEBUG, quiet=False)
	log.log(f"{Styles.bold}woodchopper v{__version__}")
	log.log("Hello, world!", text_style=Styles.bold)
