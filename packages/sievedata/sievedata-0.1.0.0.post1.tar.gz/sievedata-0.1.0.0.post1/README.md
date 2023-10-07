## Usage
```python
>python3 cli/sieve.py api --command init

api init subcommand
```

## Status
First cut to get something working. There are UX improvements to make from a dev perspective

## Future work 
We can add repeating subcommands to seperate model from command, etc. 


We can add entrypoints https://amir.rachum.com/blog/2017/07/28/python-entry-points/ so that 

```python
>python3 cli/sieve.py api --command init

api init subcommand
```

becomes 

```python
> sieve api --command init

api init subcommand
```