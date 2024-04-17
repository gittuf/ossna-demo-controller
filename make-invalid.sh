gittuf verify-ref --verbose main
echo "YOLO" >> README.md
git add README.md
git commit -S -m "YOLO"
gittuf rsl record main
gittuf rsl remote push origin
git push origin main