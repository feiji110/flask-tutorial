## Deploy to Production
assumes you have a sever that you want to deploy your application to.
### Build a distribution(发行) file.
Current standard for Python distribution is the wheel format,with the `.whl` extension.

Running `setup.py`  gives you a command line tool to issue build-related commands.
The bdist_wheel command will build a wheel distribution file.

```
$ python setup.py bdist_wheel
```
### Install the distribution file

You can find the file in dist/flaskr-1.0.0-py3-none-any.whl.
FILE NAME FORMAT: {project name}-{version}-{python tag}-{abi tag}-{platform tag}.

Copy this file to another machine,setup a new virtualenv(新的虚拟环境),then install the file with `pip`
````
$pip install flaskr-1.0.0-py3-none-any.whl
````
Pip will install your project along with itsdependencies.

Since this is a different machine,you need to run init-db again to create the database in the instance folder.
```
$ export FLASK_APP=flaskr
$ flask init-db
```


### Config the Secret Key

### Run with a Production Sever
+ Waitress: supports both Windows and Linux



## Keep Developing
 Review a few Flask and Python concepts and develop your own web applications.
 
###Reference & Comparison: 
+ [example project](https://github.com/pallets/flask/tree/1.1.2/examples/tutorial)
+ [example2](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog
)

###What can be improved
+ A detail view to show a single post.Click a post's title to go to its page.
+ Like/unlike a post.
+ Comments.
+ Tags.Clicking a tag shows all the posts with that tag.
+ A search box that filters the index page by name.
+ Paged display.Only show 5 posts per page.
+ Upload an image to go along with a post.
+ Format posts using Markdown.
+ An RSS feed of new posts.

Have fun and make awesome applications!