#! /usr/bin/python3

from argparse import ArgumentParser
from collections import namedtuple
from itertools import chain
from jinja2 import Environment, FileSystemLoader
import os
import sys
import yaml

path = os.path
FILES = -1


# data
class Navbar(namedtuple('Navbar', 'current previous next')):
    """
    Navbar is (LinkData, LinkData?, LinkData?)
    interp. current is data for link to current page, 
            previous is data for link to previous page or None if current is first,
            next is data for link to next page or None if current is last
    """
    pass

class LinkData(namedtuple('LinkData', 'href text')):
    """
    LinkData is (String, String)
    interp. href is the target url, text is the visible text that will be linked.
    """
    pass

class OldProjectData(namedtuple('ProjectData', 'full_name title body')):
    """
    ProjectData is (String, String, String)
    interp. full_name is the presentable form of the project's name
            title is the title of the project page
            body is project HTML
    """
    pass
class ProjectData(dict):
    """
    ProjectData is (String, String, String)
    interp. full_name is the presentable form of the project's name
            title is the title of the project page
            body is project HTML
    """
    def __init__(self, full_name, title, body, **kwargs):
        super(ProjectData, self).__init__(
            full_name=full_name, 
            title=title, 
            body=body, 
            **kwargs
        )
    @property
    def full_name(self):
        return self['full_name']
    @property
    def title(self):
        return self['title']
    @property
    def body(self):
        return self['body']
    def __repr__(self):
        known = ('full_name', 'title', 'body')
        return "ProjectData(%s)" % ', '.join(
            chain(
                ("%s=%r" % (k, self[k])
                 for k in known), 
                ("%s=%r" % (k, v)
                 for k,v in self.items()
                 if k not in known)
            )
        )



# functions
def parse_argv():
    """
    () -> String String String
    Produce project dir path, project name and project template file path
    from command line arguments (sys.argv).

    # proper usage
    >>> sys.argv = [
    ...     'render_project.py', 
    ...     'projects', 
    ...     '1.otter.yaml', 
    ...     'project.template'
    ... ]
    >>> parse_argv()    # doctest: +NORMALIZE_WHITESPACE
    Namespace(project_name='1.otter.yaml', 
              projects_dir='projects', 
              template_file='project.template')

    # still acceptable
    >>> sys.argv = [
    ...     'render_project.py', 
    ...     '/home/leethakz/hack-the-planet', 
    ...     '../../../../etc/shadow', 
    ...     'hash-dump.tmpltzr'
    ... ]
    >>> parse_argv()    # doctest: +NORMALIZE_WHITESPACE
    Namespace(project_name='../../../../etc/shadow', 
              projects_dir='/home/leethakz/hack-the-planet', 
              template_file='hash-dump.tmpltzr')

    # no args
    >>> sys.argv = ['render_project.py']
    >>> parse_argv()
    Traceback (most recent call last):
    SystemExit: 2

    # too few args
    >>> sys.argv = ['render_project.py', 'projects']
    >>> parse_argv()
    Traceback (most recent call last):
    SystemExit: 2

    # too many args
    >>> sys.argv = ['render_project.py', 'a', 'b', 'c', 'WHAT_IS_THIS']
    >>> parse_argv()
    Traceback (most recent call last):
    SystemExit: 2
    """
    pr = ArgumentParser(
        description="Render the given template with data of the project with the "
                    "given name, and a menu with links to all projects in the "
                    "projects directory."
    )
    for name in "projects_dir project_name template_file".split():
        pr.add_argument(name)

    return pr.parse_args()


def main(projects_dir, project_name, template_file):
    """ 
    DirPath FileName FilePath -> String
    Render the given template with data of the project with the given name,
    and a menu with links to all other projects.
    
    >>> expected_sloth = open(
    ...     'test/renderer/expected-sloth.html', 
    ...     'r'
    ... ).read()
    >>> main(
    ...     'test/renderer/projects', 
    ...     '1.sloth.yaml', 
    ...     'test/renderer/test.template'
    ... ) == expected_sloth
    True

    >>> expected_otter = open(
    ...     'test/renderer/expected-otter.html', 
    ...     'r'
    ... ).read()
    >>> main(
    ...     'test/renderer/projects', 
    ...     '2.otter.yaml', 
    ...     'test/renderer/test.template'
    ... ) == expected_otter
    True

    >>> expected_yeti = open(
    ...     'test/renderer/expected-yeti.html', 
    ...     'r'
    ... ).read()
    >>> main(
    ...     'test/renderer/projects', 
    ...     '3.yeti.yaml', 
    ...     'test/renderer/test.template'
    ... ) == expected_yeti
    True
    """
    
    jinja = Environment(
        loader=FileSystemLoader(path.abspath(path.curdir)),
        trim_blocks=True,
        lstrip_blocks=True
    )    
    projects = parse_projects(read_project_files(projects_dir))

    template = jinja.get_template(template_file)
    data = data_from_projects(projects, project_name)
    
    return template.render(data)


def read_project_files(projects_dir):
    """
    DirPath -> {String: String}
    Produce a dict of file name: file contents from the given directory path.

    Testing file reads is impractical for a script.
    """
    return {
        fname: open(
            path.join(projects_dir, fname), 
            'r'
        ).read()            
        for fname in next(os.walk(projects_dir))[FILES]
    }


def parse_projects(projects):
    """
    {String: String} -> {String: ProjectData}
    Produce a dict of parsed project data, keeping the filename associations.

    >>> parse_projects({})
    {}

    >>> parse_projects({
    ...     'otter.yaml': "full_name: Otto the otter\\n"
    ...                   "body: <p>Otto is the best ooter.</p>\\n"
    ...                   "title: Otto is a cool otter"
    ... }) # doctest: +NORMALIZE_WHITESPACE
    {'otter.yaml': ProjectData(full_name='Otto the otter',
                               title='Otto is a cool otter',
                               body='<p>Otto is the best ooter.</p>')}

    >>> parse_projects({
    ...     'a sloth': "full_name: Sylvia the sloth\\n"
    ...                "title: Sylvia is slow\\n"
    ...                "body: <span>Sylvia isnt that slow, for a sloth</span>\\n",
    ...     'b otter': "full_name: Otto the otter\\n"
    ...                "body: <p>Otto is the best ooter.</p>\\n"
    ...                "title: Otto is a cool otter",
    ...     'c yeti': "full_name: Francis the yeti\\n"
    ...               "title: Why not yeti?\\n"
    ...               "body: Francis is great at snow ball fights.\\n"
    ... }) == {
    ...     'a sloth': ProjectData(full_name='Sylvia the sloth',
    ...                             title='Sylvia is slow',
    ...                             body='<span>Sylvia isnt that slow, for a sloth</span>'),
    ...     'b otter': ProjectData(full_name='Otto the otter',
    ...                            title='Otto is a cool otter',
    ...                            body='<p>Otto is the best ooter.</p>'),
    ...     'c yeti': ProjectData(full_name='Francis the yeti',
    ...                           title='Why not yeti?',
    ...                           body='Francis is great at snow ball fights.')}
    True
    """
    return {
        k: ProjectData(**yaml.load(v))
        for k,v in projects.items()
    }


def data_from_projects(projects, project_name):
    """
    {String: String}, String -> Dict
    Produce data needed to render the project template.
    !!!

    >>> data_from_projects(
    ...     {'otter.yaml': ProjectData(full_name='Otto the otter',
    ...                                title='Otto the otter',
    ...                                body=''),
    ...     }, 
    ...     'otter.yaml'
    ... ) == {
    ...     'menu': [
    ...         LinkData(href='otter.html', text='Otto the otter'),
    ...      ],
    ...      'navbar': Navbar(current=LinkData(href='otter.html', 
    ...                                        text='Otto the otter'),
    ...                       previous=None,
    ...                       next=None),
    ...      'project': ProjectData(full_name='Otto the otter',
    ...                             title='Otto the otter',
    ...                             body=''),
    ... }
    True
    """

    data = {
        'menu': menu_from_projects(projects),
        'navbar': navbar_from_projects(project_name, projects),
        'project': projects[project_name],
    }
    return data


def menu_from_projects(projects):
    """
    {Filename: ProjectData} -> [LinkData]
    Produce a sorted list of link data, where each href points to a a project filename,
    with extension replaced by '.html', and link text is the full name of each 
    project.

    >>> menu_from_projects({})
    []
    
    >>> menu_from_projects({
    ...     'otter': ProjectData('Otto the otter', '', '')
    ... })
    [LinkData(href='otter.html', text='Otto the otter')]

    >>> menu_from_projects({
    ...     '1.abominable.yeti.yaml': ProjectData('Francis the yeti', '', ''),
    ...     '2.adorable.sloth.yaml': ProjectData('Sylvia the sloth', '', ''),
    ...     '3.floppy.otter.yaml': ProjectData('Otto the otter', '', '')
    ... }) # doctest: +NORMALIZE_WHITESPACE
    [LinkData(href='1.abominable.yeti.html', text='Francis the yeti'),
     LinkData(href='2.adorable.sloth.html', text='Sylvia the sloth'),
     LinkData(href='3.floppy.otter.html', text='Otto the otter')]
    
    """
    return [
        LinkData(
            href=link_from_filename(fname),
            text=projects[fname].full_name,
        )
        for fname in sorted(projects)
    ]


def link_from_filename(filename):
    """
    String -> String
    Replace the extension of the given filename with '.html'
    Assumes len(filename) > 0

    >>> link_from_filename('otter')
    'otter.html'
    >>> link_from_filename('.otter')
    '.otter.html'
    >>> link_from_filename('yeti.yaml')
    'yeti.html'

    """
    return path.splitext(filename)[0] + '.html'


def navbar_from_projects(project_name, projects):
    """
    String, {String: ProjectData} -> Navbar
    Produce a navigation bar with link data to projects before and after the 
    project with the given filename in a sorted list of project filenames.
    !!! add helpers

    # only
    >>> navbar_from_projects('otter', {
    ...     'otter': ProjectData('Otto', '', '')
    ... }) # doctest: +NORMALIZE_WHITESPACE
    Navbar(current=LinkData(href='otter.html', text='Otto'),
           previous=None,
           next=None)

    # first
    >>> navbar_from_projects('otter', {
    ...     'otter': ProjectData('Otto', '', ''),
    ...     'yeti': ProjectData('Francis', '', ''),
    ...     'sloth': ProjectData('Sylvia', '', ''),
    ... }) # doctest: +NORMALIZE_WHITESPACE
    Navbar(current=LinkData(href='otter.html', text='Otto'),
           previous=None,
           next=LinkData(href='sloth.html', text='Sylvia'))

    # middle
    >>> navbar_from_projects('sloth', {
    ...     'otter': ProjectData('Otto', '', ''),
    ...     'yeti': ProjectData('Francis', '', ''),
    ...     'sloth': ProjectData('Sylvia', '', ''),
    ... }) # doctest: +NORMALIZE_WHITESPACE
    Navbar(current=LinkData(href='sloth.html', text='Sylvia'),
           previous=LinkData(href='otter.html', text='Otto'),
           next=LinkData(href='yeti.html', text='Francis'))

    # last
    >>> navbar_from_projects('yeti', {
    ...     'otter': ProjectData('Otto', '', ''),
    ...     'yeti': ProjectData('Francis', '', ''),
    ...     'sloth': ProjectData('Sylvia', '', ''),
    ... }) # doctest: +NORMALIZE_WHITESPACE
    Navbar(current=LinkData(href='yeti.html', text='Francis'),
           previous=LinkData(href='sloth.html', text='Sylvia'),
           next=None)
    """
    sorted_fnames = sorted(projects)
    current_index = sorted_fnames.index(project_name)
    first, last = 0, len(sorted_fnames)-1
    return Navbar(
        current=LinkData(
            href=link_from_filename(project_name),
            text=projects[project_name].full_name
        ),
        previous=(
            None if current_index == first else
            LinkData(
                href=link_from_filename(sorted_fnames[current_index-1]),
                text=projects[sorted_fnames[current_index-1]].full_name
        )),
        next=(
            None if current_index == last else
            LinkData(
                href=link_from_filename(sorted_fnames[current_index+1]),
                text=projects[sorted_fnames[current_index+1]].full_name
        ))
    )


if __name__ == '__main__':
    a = parse_argv()

    print(main(a.projects_dir, a.project_name, a.template_file))