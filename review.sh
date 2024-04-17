export GITTUF_DEV=1
gittuf rsl remote pull origin
git fetch origin feature:feature
git checkout feature
gittuf dev authorize --from-ref feature -k ./keys/aditya main
git push origin refs/gittuf/attestations:refs/gittuf/attestations
gittuf rsl remote push origin
gh pr review --approve --body "LGTM!"