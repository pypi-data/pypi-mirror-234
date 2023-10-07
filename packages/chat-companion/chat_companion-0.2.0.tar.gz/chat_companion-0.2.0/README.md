# CLI Companion

CLI Companion is a command line tool that you can use to ask questions and get responses back from a virtual companion. You can also review previous questions and responses.

## Installation

First you need get an api key for chat-gpt.
Then you create an environment variable named `$CHATKEY`

bash
```
export CHATKEY=<your-key>
```

fish
```
set CHATKEY=<your-key>
```

Using pip

`pip install chat-companion`

Using Poetry

`poetry add chat-companion`

## Usage

run 
`companion --help` 

To see the list of commands.

```
custom commands
===============
generate_response  proof_read   review     talk     
help               resummarize  summarize  translate
```

### Talk

To ask a question, use the `talk` subcommand. For example:

```
companion talk "What is your name?"
```

### Review

To review previous questions and responses, use the `review` subcommand. This will bring up a list of previous questions. You can then select a question to view the response.