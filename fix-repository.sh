gittuf rsl annotate --skip -m "No yolo!" $(git rev-parse refs/gittuf/reference-state-log)
git revert -S --no-edit HEAD
gittuf rsl record main
gittuf rsl remote push origin
git push origin main