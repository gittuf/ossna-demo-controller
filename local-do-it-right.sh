git log
git log refs/gittuf/reference-state-log
gittuf policy list-rules
git checkout -b update-readme
echo "\nThis is a demo of gittuf!\n" >> README.md
git add README.md
git commit -S -m "Mention gittuf"
gittuf rsl record update-readme
GITTUF_DEV=1 gittuf dev authorize --from-ref update-readme -k ../ossna-demo-controller/keys/aditya main
git log refs/gittuf/reference-state-log
git log refs/gittuf/attestations
git checkout main
git merge update-readme
gittuf rsl record main
gittuf verify-ref --verbose main
echo "\nWhat if I just commit and push directly to main?\n" >> README.md
git add README.md
git commit -S -s -m "YOLO"
gittuf rsl record main
gittuf verify-ref --verbose main