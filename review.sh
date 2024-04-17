export GITTUF_DEV=1
gittuf rsl remote pull origin
git fetch origin feature:feature
git checkout feature
gittuf dev authorize --from-ref feature -k ./keys/ossna-1 main
git push origin refs/gittuf/attestations:refs/gittuf/attestations
gh pr review --approve --body "LGTM!"