# oceano_algos
> Library for algorithms to be used in Airflow and not only.
> Storing at: https://pypi.org/project/oceano-algos/

## Install
```bash
pip install --upgrade oceano-algos
```
(make sure the newest version was downloaded)

# help links:

nbdev template: https://github.com/fastai/nbdev_template
example of nbs_build_lib: https://youtu.be/r4RuVI-r5ZI
how to ssh git clone: https://youtu.be/5Ck07BJDXTE
how to do push to PyPI: https://youtu.be/ji5nkIiGHrU


# How to use:
1. run ```git checkout -n <new branch name>```
2. do some changes locally
3. open terminal and run ```make all```
4. run ```git add . ```
5. run ```git commit -m '<commit text>```
6. ```git push```
7. visit the merge request page and check if pipeline's jibs succeded, than optionally approve ```push to pypi``` job which will push merged new version of library to PyPI 
8. merge in the main page of merge request
