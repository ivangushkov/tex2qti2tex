## tex2qti2tex

Scripts developed for parsing questions back and forth between qti and faceit tex format. Still work in progress and further work is detailed farther down.


### tex2qti pipeline

The tex2qti takes a set of questions (for now multiple choice) on the face it format, extracts the elements, parses them from LaTeX to md using pandoc, and converts them to qti quizes using the text2qti library.

Run tex2qti.py script for an example. Generates the sample_assesment.zip qti assesment/quiz from LinSys_MC.tex

### qti2tex pipeline

The qti2tex pipeline takes a set of items/assesments and extracts the question information from them, and writes it on the faceit tex format. The pipeline is divided into 2 modules, the "assesment scanner" and the "content extractor". 

The "scanner" is question nr and type agnostic, it simply finds iterable objects which contain all the question content of an xml file. Note that the qti version can be passed as argument to the scanner, which allows for extracting from multiple versions of qti (only 3.0 implemented atm).

The "content extractor" takes the iterables from the "scanner", and finds the number and types of questions, and saves them as question objects. Each object has a write function which when passed a tex file will append the question to it on the faceit format. Only multiple choice is implemented atm, but the architecture is there to readily admit more question types.

Run qti2tex_pipeline.py script for an example. Generates the fateit_quiz.tex file from data/items/composition_of_water_qti3.xml

### Further Work

**tex2qti:**
- preview the generated qti assesment in a qti program
- clean up the functions and make them more robust/general
- implement conversion to qti v3.0

**qti2tex:**
- implement more versions of qti (2.2, 1.2?)
- implement more types of questions (essay?)
- implement translation to LaTeX
- test on bigger/more challenging datasets to ensure robust behaviour