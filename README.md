# paper-demo
Demo paper for DaPaWriMo with logging tools.

### Initial setup: 

1) Make a repository for your paper manusript, say, somewhere in the DAWN-CPH team space (https://github.com/dawn-cph/).

2) Copy the `texcount.pl` and `texcount.py` scripts from this demo repo to your working repo

3) Write your manuscript in a LaTeX file (e.g., "ms.tex").  The demo here provides the AASTEX6.2 macros.

### Log your status

1) Check that `texcount.pl` runs without errors:

    `./texcount.pl ms.tex`
   
2) Log the word count status to a file & plot):

    `./texcount.py ms.tex [-plot-only] [-log-only]`
  
3) Commit and push the updated logs (and of course your manuscript, figures, etc. as well)

    `git commit -m "[comment, e.g. update logs]" word_count.csv word_count.log`
  
    `git push`

4) Get a coffee and cheer on your colleagues
  
