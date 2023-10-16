#! /usr/bin/env python3

# #################################################################################### #
#                                                                                      #
# Main: MapTasker entry point                                                          #
#                                                                                      #
# GNU General Public License v3.0                                                      #
# Permissions of this strong copyleft license are conditioned on making available      #
# complete source code of licensed works and modifications, which include larger works #
# using a licensed work, under the same license. Copyright and license notices must be #
# preserved. Contributors provide an express grant of patent rights.                   #
#                                                                                      #
# #################################################################################### #

from maptasker.src import mapit


def main():
    """
    Kick off the main program: mapit.pypwd

    """

    # Call the core function passing an empty filename
    return_code = mapit.mapit_all("")
    exit(return_code)


if __name__ == "__main__":
    # FOR DEVELOPMENT ONLY  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # The following outputs a file "maptasker_profile.txt" with a breakdown of
    # function calls

    # import cProfile
    # import pstats

    # cProfile.run("main()", "results")
    # with open("maptasker_profile.txt", "w") as file:
    #     profile = pstats.Stats("results", stream=file).sort_stats("ncalls")
    #     profile.print_stats()
    #     file.close()

    main()
