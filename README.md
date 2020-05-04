# Getting started on a data analysis project on GenomeDK


How to set up a github account and fork this repository...


Link to slurm-jupyter, terminal tutorials, git tuturials, github ssh etc.

Add example pandas notebooks.


## This page is work in progress!

Research must be reproducible. It must be documented to an extent that somewone else is able repeat your analysis. Why this is.

That it adds value beyond your own project, becuse it allows other to use and learn from what you did and build on top of your acheievemnts. 

For comments and suggestions for improvement of this page, please [send me an email](mailto:kaspermunch@birc.au.dk).


I will assume some familiarity with a terminal.


## Install Python on your own machine

You shuold a distribution of Python called *Anaconda*. Anaconda is simply an easy way of installing Python on Windows, macOS (Mac), and Linux, but it comes with the conda package management system (see below). To install Anaconda, head to [this](https://www.anaconda.com/download) site. Scroll down a bit and click the big green Download button where it says **Python 3.7 version**. When the download has completed, you should follow the platform specific instructions:

Install Anaconda python your local machine.  If you are on a Windows machine you also need to tick the box to add Anaconda python to your PATH when prompted.

* **For Windows:** Double-click the `.exe` file you just downloaded and follow the instructions on the screen. Say yes when asked if want to install Visual Studio Code. The installer will also ask you if you want to download and install a program called Visual Studio Code. Do that too.
* **For OSX:** Double-click the `.pkg` file you just downloaded and follow the instructions on the screen. Make a default installation. The installer will also ask you if you want to download and install a program called Visual Studio Code. Do that too.

If you are on a Mac or Limux machine, you can use to default terminal application. If you are on a Windwos macinne, you need to download and the newest version of Powershell. You find see how to do that on this page under "Installing the MSI package". Now open the newly installed Powershell and run: conda init powershell. Close Powershell and open it again. Now you have access to conda to create environments if you like. 

> In addition, you can also install [mobaxterm](https://mobaxterm.mobatek.net/). It also has come nice file browsing capabilities.

When ever I refer to "the terminal" below, it means Poweshell if you are on windows, and the Terminal app if you are on Mac.


## The terminal

There are some exelent quick tutorials online that introduces the most basic commands in a Linus terminal.

However, here are basics. First of all, a terminal lets you execute commands on your computer. You simply type the command you want and then hit enter. The place where you type is called a prompt and it may look a little different depending on which terminal emulator you use. In this book we represent the prompt with the character `$`.

When you open the terminal you'll be located in a folder. You can see which folder you are in by typing `pwd`, and then press `Enter` on the keyboard. When you press `Enter` you tell the terminal to execute the command you just wrote. In this case, the command you typed simply tells you the path of the folder we are in. If I do it I get:

    $ pwd
    /Users/kasper/programming

So right now I am in the folder `programming`. `/Users/kasper/programming` is the "full address" of the folder with dashes (or backslashes on windows) separating folders. So `programming` is a subfolder of `kasper` which is a subfolder of `Users`. That way you not only know which folder you are in but also where that folder is. Let us see what is in this folder. You type the `ls` command (l as in Lima and s as in Sierra). When I do that and press `Enter` I get:

    $ ls
    notes projects

It seems that there are two other folders, one called `notes` and another called `projects`. If you are curious about what's inside `notes` you can "walk" into the folder with the `cd` command. To use this command you must specify which folder we want to walk into (in this case `notes`). We do this by typing `cd`, then a space and the then name of the folder. When I press enter I get:


    $ cd notes
    $


It seems that nothing really happened, but if I run the `pwd` command now to see which folder I am in, I get:

```
$ pwd
/Users/kasper/programming/notes
```

Just to keep track of what is happening: before we ran the `cd` command we were in the directory `/Users/kasper/programming` folder, and now we're in `/Users/kasper/programming/notes`. This means that we can now use the `ls` command to see what is in the `notes` folder:

    $ ls
    $


Again it seems like nothing happened. Well, `ls` do not show anything if the folder we are in is empty. So `notes` must be empty. Let us go back to where we came from. To
walk "back" or "up" to `/Users/kasper/programming` we again use the `cd` command, but this time we do not tell it to go to a specific folder. Instead, we use the special name `..` to say that we wish to go to the parent folder called `programming`, i.e. the folder we just came from:

    $ cd ..
    $ pwd
    /Users/kasper/programming

Now when we run the `pwd` command we see that we are back where we started. Let us see if the two folders are still there:


    $ ls
    notes projects

They are! You are now able to use navigate your folders and see what is in them. 




## Getting an account on the cluster

The cluster is called GenomeDK and has its own [website](https://genome.au.dk) with lots of information and ducumentation.To get an account on the cluster, you [request one here](https://genome.au.dk/docs/getting-started/#request-access). Below `username` will represent your user name.

On the cluster you have a home folder that only you have access to. Data projects, collaborative or not belongs in project folders. If you do a project, we will set up a dedicated project folder for this. 

## Connecting to the cluster

You connect to the cluster from the terminal by executing this command:

    ssh usernmae@login.genome.au.dk

You must set up your ssh connection to the cluster so you can connect securely without typing the password every time. First see if you have these two authentication files on your local machine:

    ~/.ssh/id_rsa
    ~/.ssh/id_rsa.pub

if not, you generate a pair of authentication keys like this. Do not enter a passphrase when prompted - just press enter:

    ssh-keygen -t rsa

Now use `ssh` to create a directory `~/.ssh` on the cluster (assuming your username on the cluster is donald):

    ssh donald@login.genome.au.dk mkdir -p .ssh

Finally append the public key on your local machine to the file `.ssh/authorized_keys` on the cluster and enter the password one last time (replace donald with your cluster user name):

    cat ~/.ssh/id_rsa.pub | ssh donald@login.genome.au.dk 'cat >> .ssh/authorized_keys'

From now on you can log into the cluster from your local machine without being prompted for a password.

## Install Python on the cluster

You need to install miniconda if you do not already have Anaconda Python installed in your cluster home dir. Run these commands in your cluster home dir. They will download and install miniconda for you. Say yes when it asks if it should run conda init for you.

  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  bash Miniconda3-latest-Linux-x86_64.sh


## Conda

You need to install packages and programs for use in your analyses and pipelines. Sometimes, however, the versions of packages you need for one project conflicts with the versions you need for other projects that you work on in parallel. Such conflicts seem like an unsolvable problem. Would it not be fantastic if you could create a small world, insulated from the rest of your Anaconda installation. Then that small world could only contain the packages you needed for a single project. If each project had its own isolated world, then there would be no such conflicts. Fortunately, there is a tool that lets you do just that, and its name is Conda. The small worlds that Conda creates are called "environments," and you can create as many as you like, and then switch between them as you switch between your bioinformatics projects. Conda also downloads and installs the packages for you and makes sure that the packages you install in each environment are compatible.  It even makes sure that packages needed by packages  (dependencies) are installed. 

Conda lets you install mutually compatible versions of software and libraries in an enviromment for your project. By creating an enviromnet for each project, the libraries installed for each project do not interfere. 

## Creating an environment on your local machine

When you install Anaconda or Miniconda, Conda makes a single base environment for you. It is called "base" and this is why it says "(base)" at your terminal prompt. You need a conda enviromnet for you project on both your local machine and on the cluster. Lets call both of them 'bircproject' (you can call it anything you like).

The environmnet on your local machine does not need a lot of packages since it mainly serve to let you connect to the cluster. This creates the enviromnet and installs `openssl` and `slurm-jupyter` from my conda chanel:

    conda create -n bircproject -c kaspermunch slurm-jupyter openssl

## Creating an environment on the cluster



Usefull conda packages for bioinformatics / population genomic analysis

- gwf (grid workflow)
- jupyter jupyterlab jupyter_contrib_nbextensions rise nbconvert (jupyter)
- numpy pandas (arrays, matrices, data frames)
- matplotlib seaborn ipympl ipywidgets nodejs mpld3 plotly (plotting)
- cartopy shapely fiona (plotting maps)
- scipy scikit-learn scikit-bio statsmodels (stats, models, and machine learning)
- ete3 (trees)
- biopython (bread and butter bioinformatics)
- pyfaidx tabix samtools h5py (data storage and indexing)
- networkx (network graphs)
- mygene (gene annotation)
- msprime  (simulation)
- scikit-allel vcftools (workign with VCF files)

My standard environment

    conda create --name NAME -c gwforg -c etetoolkit -c anaconda -c conda-forge -c bioconda python=3.7 gwf jupyter jupyterlab jupyter_contrib_nbextensions rise nbconvert numpy scipy pandas h5py scikit-learn scikit-bio statsmodels matplotlib seaborn ipympl ipywidgets nodejs mpld3 plotly cartopy shapely fiona ete3 biopython pyfaidx networkx mygene msprime openblas scikit-allel pylint vcftools tabix samtools pip setuptools wheel twine conda-verify


Enable matplotlib extensions for jupyter lab:

    conda activavte NAME

    jupyter labextension install @jupyter-widgets/jupyterlab-manager
    jupyter labextension install jupyter-matplotlib


## Backup on the cluster

link to the backup information

## Git and GitHub


## Jupyter

<script src="https://gist.github.com/kaspermunch/3819068502531fc4ac2e732957916a0d.js"></script>



## Jupyter on the cluster

https://github.com/kaspermunch/slurm-jupyter

    git clone example notebooks

## VS Code on the cluster


## Building workflows with gwf GWF


## Distributing conda packages and Docker images
