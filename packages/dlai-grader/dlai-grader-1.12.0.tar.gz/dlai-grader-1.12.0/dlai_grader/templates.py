from textwrap import dedent
from typing import Dict


def load_templates() -> Dict[str, str]:
    specialization = input("Name of the specialization: ")
    course = input("Number of the course: ")
    week = input("Number of the week: ")
    version = input("Version of the grader (leave empty for version 1): ")
    version = "1" if not version else version

    dockerfile = """
	FROM continuumio/miniconda3@sha256:d601a04ea48fd45e60808c7072243d33703d29434d2067816b7f26b0705d889a

	RUN apk update && apk add libstdc++

	COPY requirements.txt .

	RUN pip install -r requirements.txt && \
	rm requirements.txt

	RUN mkdir /grader && \ 
	mkdir /grader/submission

	COPY .conf /grader/.conf
	COPY data/ /grader/data/
	COPY solution/ /grader/solution/
	COPY entry.py /grader/entry.py
	COPY grader.py /grader/grader.py

	RUN chmod a+rwx /grader/

	WORKDIR /grader/

	ENTRYPOINT ["python", "entry.py"]
    """

    conf = f"""
	ASSIGNMENT_NAME=C{course}W{week}_Assignment
	IMAGE_NAME={specialization}c{course}w{week}-grader
	GRADER_VERSION={version}
	TAG_ID=V$(GRADER_VERSION)
	SUB_DIR=mount
	MEMORY_LIMIT=4096
	LINUX_UPLOAD_DIR='/mnt/c/Users/Andres/dlai/upload'
	MAC_UPLOAD_DIR='/Users/andreszarta/Desktop/upload-temp'
    """

    makefile = """
	.PHONY: learner build entry submit-solution upgrade test grade mem zip clean upload move-zip move-learner tag undeletable versioning upgrade sync

	include .conf

	PARTIDS = ""
	OS := $(shell uname)

	sync:
		cp mount/submission.ipynb ../$(ASSIGNMENT_NAME)_Solution.ipynb
		cp learner/$(ASSIGNMENT_NAME).ipynb ../$(ASSIGNMENT_NAME).ipynb

	learner:
		dlai_grader --learner --output_notebook=./learner/$(ASSIGNMENT_NAME).ipynb

	build:
		docker build -t $(IMAGE_NAME):$(TAG_ID) .

	debug:
		docker run -it --rm --mount type=bind,source=$(PWD)/mount,target=/shared/submission --mount type=bind,source=$(PWD),target=/grader/ --entrypoint ash $(IMAGE_NAME):$(TAG_ID)

	submit-solution:
		cp solution/solution.ipynb mount/submission.ipynb

	versioning:
		dlai_grader --versioning

	tag:
		dlai_grader --tag

	undeletable:
		dlai_grader --undeletable

	upgrade:
		dlai_grader --upgrade

	test:
		docker run -it --rm --mount type=bind,source=$(PWD)/mount,target=/shared/submission --mount type=bind,source=$(PWD),target=/grader/ --entrypoint pytest $(IMAGE_NAME):$(TAG_ID)

	grade:
		dlai_grader --grade --partids=$(PARTIDS) --docker=$(IMAGE_NAME):$(TAG_ID) --memory=$(MEMORY_LIMIT) --submission=$(SUB_DIR)

	mem:
		memthis $(PARTIDS)

	zip:
		zip -r $(IMAGE_NAME)$(TAG_ID).zip .

	clean:
		find . -maxdepth 1 -type f -name "*.zip" -exec rm {} +
		docker rm $$(docker ps -qa --no-trunc --filter "status=exited")
		docker rmi $$(docker images --filter "dangling=true" -q --no-trunc)

	upload:
		coursera_autograder --timeout 1800 upload --grader-memory-limit $(MEMORY_LIMIT) --grading-timeout 1800 $(IMAGE_NAME)$(TAG_ID).zip $(COURSE_ID) $(ITEM_ID) $(PART_ID)

	move-zip:
		if [[ "$(OS)" == "Darwin" ]];    \
		then    \
			mv $(IMAGE_NAME)$(TAG_ID).zip $(MAC_UPLOAD_DIR);    \
		else    \
			mv $(IMAGE_NAME)$(TAG_ID).zip $(LINUX_UPLOAD_DIR);    \
		fi

	move-learner:
		if [[ "$(OS)" == "Darwin" ]];    \
		then    \
			cp learner/$(ASSIGNMENT_NAME).ipynb $(MAC_UPLOAD_DIR);    \
		else    \
			cp learner/$(ASSIGNMENT_NAME).ipynb $(LINUX_UPLOAD_DIR);    \
		fi
    """

    grader_py = """
	from types import ModuleType, FunctionType, FunctionType
	from typing import Dict, List, Optional
	from dlai_grader.grading import test_case, object_to_grade
	from dlai_grader.types import grading_function, grading_wrapper


	def part_1(
		learner_mod: ModuleType, solution_mod: Optional[ModuleType]
	) -> grading_function:
		@object_to_grade(learner_mod, "learner_func")
		def g(learner_func: FunctionType) -> List[test_case]:

			t = test_case()
			if not isinstance(learner_func, FunctionType):
				t.failed = True
				t.msg = "learner_func has incorrect type"
				t.want = FunctionType
				t.got = type(learner_func)
				return [t]

			cases: List[test_case] = []

			return cases

		return g


	def handle_part_id(part_id: str) -> grading_wrapper:
		grader_dict: Dict[str, grading_wrapper] = {
			"": part_1,
		}
		return grader_dict[part_id]
	"""

    entry_py = """
	from dlai_grader.config import Config
	from dlai_grader.compiler import compile_module
	from dlai_grader.io import read_notebook, copy_submission_to_workdir, send_feedback

	from dlai_grader.notebook import (
		notebook_to_script,
		keep_tagged_cells,
		notebook_is_up_to_date,
		notebook_version,
		cut_notebook,
		partial_grading_enabled,
	)
	from dlai_grader.grading import compute_grading_score, graded_obj_missing
	from grader import handle_part_id


	def main() -> None:
		c = Config()

		copy_submission_to_workdir()

		try:
			nb = read_notebook(c.submission_file_path)
		except Exception as e:
			send_feedback(
				0.0,
				f"There was a problem reading your notebook. Details:\\n{str(e)}",
				err=True,
			)

		if not notebook_is_up_to_date(nb):
			msg = f"You are submitting a version of the assignment that is behind the latest version.\\nThe latest version is {c.latest_version} and you are on version {notebook_version(nb)}."

			send_feedback(0.0, msg)

		transformations = [cut_notebook(), keep_tagged_cells()]

		for t in transformations:
			nb = t(nb)

		script = notebook_to_script(nb)

		try:
			learner_mod = compile_module(script, "learner_mod", verbose=False)
		except Exception as e:
			send_feedback(
				0.0,
				f"There was a problem compiling the code from your notebook. Details:\\n{str(e)}",
			)

		solution_script = notebook_to_script(read_notebook(c.solution_file_path))
		solution_mod = compile_module(solution_script, "solution_mod", verbose=False)

		g_func = handle_part_id(c.part_id)(learner_mod, solution_mod)

		try:
			cases = g_func()
		except Exception as e:
			send_feedback(
				0.0,
				f"There was an error grading your submission. Details:\\n{str(e)}",
				err=True,
			)

		if graded_obj_missing(cases):
			additional_msg = ""
			if partial_grading_enabled(nb):
				additional_msg = "The # grade-up-to-here comment in the notebook might be causing the problem."

			send_feedback(
				0.0,
				f"Unable to find object required for grading in your code.\\n{additional_msg}",
				err=True,
			)

		score, feedback = compute_grading_score(cases)

		send_feedback(score, feedback)


	if __name__ == "__main__":
		main()
	"""

    template_dict = {
        "dockerfile": dedent(dockerfile[1:]),
        "makefile": dedent(makefile[1:]),
        "conf": dedent(conf[1:]),
        "grader_py": dedent(grader_py[1:]),
        "entry_py": dedent(entry_py[1:]),
    }

    return template_dict
