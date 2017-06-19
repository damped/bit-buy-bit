# Bit-Buy-Bit
Bitcoin trading bot using Tensorflow (still in planning phase)


## Instalation
### Cloning the Repo

Follow these instructions https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/


First generate a new ssh key. (Press Enter for default directory and Enter for no password)
```shell
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# Start ssh agent:
eval "$(ssh-agent -s)"
# Add ssh key:
ssh-add ~/.ssh/id_rsa
```

Then go to github and copy your key into the settings menue:
```shell
cat ~/.ssh/id_rsa.pub
```

And clone it into your ~ (home) directory
```shell
git clone git@github.com:damped/bit-buy-bit.git
```


