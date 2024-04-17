git config --local user.name "Aditya Sirish"
git config --local user.email "aditya@example.com"
git config --local gpg.format ssh
git config --local user.signingkey "/home/saky/lab/gittuf/ossna-demo-controller/keys/aditya"
gittuf rsl annotate --skip -m "No yolo!" $(git rev-parse refs/gittuf/reference-state-log)
git revert -S --no-edit HEAD
gittuf rsl record main
gittuf rsl remote push origin
git push origin main