julianbuccat@Julians-MacBook-Pro-4 .ssh % ls -lA
total 56
drwx------  3 julianbuccat  staff   96 Mar 17 15:47 agent
-rw-------@ 1 julianbuccat  staff  149 Mar  5 12:15 config
-rw-------@ 1 julianbuccat  staff  444 Mar  5 10:53 id_ed25519
-rw-r--r--@ 1 julianbuccat  staff   82 Mar  5 10:53 id_ed25519.pub
-rw-------@ 1 julianbuccat  staff  411 Mar  5 12:11 id_ed25519_github
-rw-r--r--@ 1 julianbuccat  staff  100 Mar  5 12:11 id_ed25519_github.pub
-rw-------@ 1 julianbuccat  staff  828 Mar  5 12:13 known_hosts
-rw-r--r--@ 1 julianbuccat  staff   92 Mar  5 12:02 known_hosts.old

---

agent - background process that holds private keys in memory, so SSH can authenticate without asking for your passphrase on every command

where SSH keys are stored on macOS/Linux
    - default directory: ~/.ssh/
    - private keys (never share):
        - id_ed25519
        - id_ed25519_github
    - public keys (safe to share):
        - id_ed25519.pub
        - id_ed25519_github.pub

config - per-host SSH rules and aliases
    - used to define Host, HostName, User, IdentityFile, AddKeysToAgent, UseKeychain, etc.
Ex:
    Host github.com
      HostName github.com
      User git
      IdentityFile ~/.ssh/id_ed25519_github
      AddKeysToAgent yes
      UseKeychain yes

known_hosts - stores server host keys for hosts you have connected to before
    - entries look like: github.com ssh-ed25519 AAAAC3Nza...
    - SSH computes a fingerprint from the host key and compares it to known_hosts
    - if fingerprint does not match, SSH warns:
        WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!
    - SSH comparing Fingerprint to server host key effectively protect you against MITM attacks

important distinction
    - your private key identifies you to the server
    - known_hosts host key verifies the server you are connecting to

agent/ directory
    - agent sockets and metadata for ssh-agent process communication
    - does not replace private key files on disk

