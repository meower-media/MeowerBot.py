# Help

This is a builtin help cog in MeowerBot.py. It defines the help command and the help menu.

## Help Command

You can use the help command by sending `{prefix} help <page>` to any chat the bot is in.

## Help Menu

The general look of the menu is this.

```
-- [ {cog name} ] --
!{command name} <p: any> 

-- [ Unsorted ] --
!{command name} <{argument name}: {argument type}>
    !{command name} {subcommand name} <{argument name}: {argument type}> 



!{command name} 
```

here is a real example

```
-- [ Help ] --
!help <p: any> 

-- [ Unsorted ] --
!test <a: any> 
    !test sub <a: any> 



!reloadtime
```

The menu is split into two sections, the cog section and the unsorted section. The cog section is a list of all the cogs in the bot, and the unsorted section is a list of all the commands that are not in a cog. 

The cog sections also have a list of all the commands in that cog.

This can be used to create sections.


## Creating the command within your bot

To create the command within your bot, you need to add the following code to your bot.

- 1: Import the help command from the MeowerBot.ext.help module.
	```py
	from MeowerBot.ext.help import Help
	```

- 2: Create the Help object

	```py
	help = Help(bot)
	```

- 3: Add the help command to your bot

	```py
	bot.register_cog(help)
	```

