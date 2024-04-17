git checkout -b feature
echo "Let's do it right." >> README.md
git add README.md
git commit -S -m "Doing it right this time!"
gittuf rsl record feature
gittuf rsl remote push origin
git push origin feature
gh pr create --title "Doing it right this time" --body "Apologies about the YOLO-age"