#!/usr/local/bin/python3

import json
import sys
import subprocess
from multiprocessing import Pool
from time import sleep


class Recipe(object):
    """
    Class to store information about a recipe.
    """

    dish_name = None
    author = None
    source = None
    ingredients = []
    method = []
    notes = None

    def __init__(self, filename):
        """
        Create the recipe object from a given json file.
        IN:
            filename: name of existing json file containing recipe information
        """
        with open(filename, "r") as file:
            recipe = json.load(file)
        self.dish_name = recipe["dish_name"]
        self.author = recipe["author"]
        self.source = recipe["source"]
        self.ingredients = recipe["ingredients"]
        self.method = recipe["method"]
        self.notes = recipe["notes"]

    def export(self, outfile):
        """
        Creates a latex file for the recipe.
        IN:
            outfile: name of file for output latex
        """
        texfile = open(outfile, "w")
        # make header for initial document setup
        texfile.write(
            "\\documentclass[12pt]{article}\n\\usepackage[margin=1in,landscape]{geometry}\n"
        )
        texfile.write("\\usepackage{multicol}\n")
        texfile.write("\\usepackage{fontspec}\n")
        texfile.write("\\setmainfont[Ligatures={Common}]{Hoefler Text}\n")
        texfile.write("\\author{" + self.author + "}\n")
        texfile.write("\\title{" + self.dish_name + "}\n")
        texfile.write("\\date{}\n")  # empty date
        texfile.write("\\begin{document}\n\\begin{multicols*}{2}\n\\maketitle\n\n")

        # source
        if self.source:
            texfile.write("Source: {}\n\n".format(self.source))

        # notes
        if self.notes:
            texfile.write("\\section{Notes}\n")
            texfile.write("\n{}\n\n".format(self.notes))

        # ingredients
        texfile.write("\\section{Ingredients}\n\n\\begin{itemize}\n")
        for ingredient in self.ingredients:
            texfile.write("    \\item {}\n".format(ingredient))
        texfile.write("\\end{itemize}\n\n")

        # method
        texfile.write("\\section{Method}\n\n\\begin{enumerate}\n")
        for step in self.method:
            texfile.write("    \\item {}\n".format(step))
        texfile.write("\\end{enumerate}\n\n")

        texfile.write("\\end{multicols*}\n")
        texfile.write("\\end{document}\n")
        texfile.close()

    def render(self, outfile):
        """
        Render the recipe using pdflatex.
        """
        subprocess.run(["xelatex", outfile])


def json_to_pdf(filepath):
    """
    Function which leverages the above recipe class to perform all of the
    acitons needed to convert a recipe from JSON format to the PDF. This exists
    to help make multiproccessing cleaner.
    """
    dish = Recipe(filepath)
    dish.export(filepath.replace(".json", ".tex"))
    dish.render(filepath.replace(".json", ".tex"))


if __name__ == "__main__":
    # start a pool of 4 workers to render the recipes
    # example call: python3 recipe_render.py recipe1.json recipe2.json
    Pool(4).map(json_to_pdf, sys.argv[1:])
