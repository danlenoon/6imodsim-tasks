#Lenon, Danielle Laurence B. | CS-301 | 7.11.2025

studentnames <- c('Aahron Becker', 'Aebram Bestilla', 'Aeritha Betins',
                  'Anoveha Bistonas', 'Bellina Broskerson', 'Black Brown',
                  'Beonah Brunos', 'Blessie Castro', 'Casper Casun',
                  'Cevine Cerel', 'Clhayde Croast', 'Comer Cortez',
                  'Coleine Cuervinet', 'Dasmari De Neon', 'Delle De Omar',
                  'Eli De Paris', 'Franceen Ebano', 'Franck Eran',
                  'Gearold Finez', 'Gergona Frinol')

studentnumbers <- c(101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
                    112, 113, 114, 115, 116, 117, 118, 119, 120)

coursedegreeprogram <- c('BS Computer Science', 'BS Computer Science',
                         'BS Computer Science', 'BS Computer Science',
                         'BS Computer Engineering', 'BS Computer Science',
                         'BS Computer Science', 'BS Computer Engineering',
                         'BS Computer Science', 'BS Computer Science',
                         'BS Computer Engineering', 'BS Computer Science',
                         'BS Computer Science', 'BS Computer Engineering',
                         'BS Computer Science', 'BS Computer Science',
                         'BS Computer Engineering', 'BS Computer Science',
                         'BS Computer Science', 'BS Computer Engineering')

yearlevel <- c('1st Year', '1st Year', '3rd Year', '4th Year', '2nd Year',
               '1st Year', '2nd Year', '1st Year', '2nd Year', '3rd Year',
               '2nd Year', '3rd Year', '2nd Year', '3rd Year', '3rd Year',
               '4th Year', '4th Year', '4th Year', '1st Year', '4th Year')

subjecttaken <- c('Data Structures and Algorithms', 'Cloud Computing',
                 'Introduction to Networks', 'PE 1',
                 'Theology 2', 'Theology 1', 'Linear Algebra',
                 'Differential Calculus', 'Integral Calculus',
                 'Purposive Communication', 'PE 2', 'PE 3', 'PE 4',
                 'Science, Technology, and Society',
                 'Design and Analysis of Algorithms',
                 'Object Oriented Programming',
                 'Computer-Aided Drafting',
                 'Automata Theory and Formal Languages',
                 'Web Programming', 'Ethics')

stud.data <- data.frame(StudentNames = studentnames,
                        StudentNumbers = studentnumbers,
                        CourseDegreeProgram = coursedegreeprogram,
                        YearLevel = yearlevel,
                        SubjectTaken = subjecttaken,
                        stringsAsFactors = FALSE)

print(stud.data)