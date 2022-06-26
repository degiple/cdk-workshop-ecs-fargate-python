
# Update PS1
PS1='\n\[[01;32m\]\u\[[00m\] \[[01;34m\]\w\[[00m\]$(__git_ps1 " (%s)") \n$ '

# Tab completion for AWS CLI
complete -C '/usr/local/bin/aws_completer' aws

# Tab completion for AWS CDK CLI
function _cdk_completer {
  STACK_CMDS="list synthesize bootstrap deploy destroy diff metadata init context docs doctor"

  if [ "$3" == "cdk" ]; then
    COMPREPLY=($(compgen -W "$STACK_CMDS" $2))
  elif [[ -d "cdk.out" ]] && ! [[ "$2" == "-"* ]]; then
    TEMPLATES=$(ls -1 cdk.out/*.template.json | awk '{split($0,t,/\/|\./); print t[3]}')
    COMPREPLY=($(compgen -W "$TEMPLATES" $2))
  else
    COMPREPLY=()
  fi
}
complete -F _cdk_completer cdk
