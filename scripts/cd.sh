function cd
{
  echo  $#
  if [[ $# -eq 2 ]];
  then
        source=$1
        target=$2
        if [[ -z $source || -z $target ]];
        then
                echo "Error: Usage  cd-substitute-dirs {search} {substitution}"
                return
        fi

        newdir=$(echo `pwd` |sed s/$source/$target/g)
        if [[ $newdir == `pwd` ]];
        then
          echo "String \"${source}\" not found in path.  Directory not changed."
        else
          pushd $newdir
        fi
  else
    pushd "$@"  # changes default behaviour - cd with no args is now 'cd -'
  fi
}
