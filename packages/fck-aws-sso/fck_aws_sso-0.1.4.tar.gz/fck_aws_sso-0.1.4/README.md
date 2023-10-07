# A CLI tool to automate AWS SSO login. It uses selenium with chrome under the hood.

### 1. Install with `pipx`

```
pipx install fck-aws-sso
```

### 2. Run first time with `--no-headless`

You need that to save your browser user data. `BROWSER=true` is hack so aws sso won't open browser. Browser will be opened by `fck-aws-sso`.

```
BROWSER=true aws sso login | fck-aws-sso --no-headless
```

### 3. Add to `.bashrc` or `.zshrc`

```
BROWSER=true aws sso login | fck-aws-sso
```

### 4. Forget that you ever had to login to AWS SSO manually.

## How it works

Script reads `aws sso login` output from stdin and parses it. Then it opens chrome with user data dir and navigates to AWS SSO login page. After that it fills the form and submits it. Finally it waits for aws sso to confirm login and then it closes chrome. There is default headless mode so you won't see anything. If you want to see what's going on you can use `--no-headless` option. It will open chrome and you will see what's going on.

## Prerequisites

You need `google-chrome` installed and in your `PATH`.
