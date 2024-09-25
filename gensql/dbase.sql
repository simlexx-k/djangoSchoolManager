--
-- File generated with SQLiteStudio v3.4.4 on Wed Sep 25 22:41:29 2024
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: administrator_academiccalendar
CREATE TABLE IF NOT EXISTS "administrator_academiccalendar" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "description" text NOT NULL, "start_date" date NOT NULL, "end_date" date NOT NULL, "event_type" varchar(10) NOT NULL);

-- Table: administrator_attendance
CREATE TABLE IF NOT EXISTS "administrator_attendance" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" date NOT NULL, "learner_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED, "status" varchar(10) NOT NULL);

-- Table: administrator_curriculum
CREATE TABLE IF NOT EXISTS "administrator_curriculum" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "description" text NOT NULL, "grade_id" bigint NOT NULL REFERENCES "learners_grade" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: administrator_curriculum_subjects
CREATE TABLE IF NOT EXISTS "administrator_curriculum_subjects" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "curriculum_id" bigint NOT NULL REFERENCES "administrator_curriculum" ("id") DEFERRABLE INITIALLY DEFERRED, "subject_id" integer NOT NULL REFERENCES "exams_subject" ("subject_id") DEFERRABLE INITIALLY DEFERRED);

-- Table: administrator_teacher
CREATE TABLE IF NOT EXISTS "administrator_teacher" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "employee_id" varchar(20) NOT NULL UNIQUE, "date_of_birth" date NOT NULL, "email" varchar(254) NOT NULL, "date_joined" date NOT NULL, "address" text NULL, "is_class_teacher" bool NOT NULL, "phone_number" varchar(15) NULL);
INSERT INTO administrator_teacher (id, name, employee_id, date_of_birth, email, date_joined, address, is_class_teacher, phone_number) VALUES (1, 'Simon Kosgei', '933146', 886377600000, 'kiptookosgeisimon@gmail.com', 1613001600000, NULL, 0, NULL);

-- Table: administrator_teacher_subjects
CREATE TABLE IF NOT EXISTS "administrator_teacher_subjects" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "teacher_id" bigint NOT NULL REFERENCES "administrator_teacher" ("id") DEFERRABLE INITIALLY DEFERRED, "subject_id" integer NOT NULL REFERENCES "exams_subject" ("subject_id") DEFERRABLE INITIALLY DEFERRED);

-- Table: administrator_teacherassignment
CREATE TABLE IF NOT EXISTS "administrator_teacherassignment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "grade_id" bigint NOT NULL REFERENCES "learners_grade" ("id") DEFERRABLE INITIALLY DEFERRED, "subject_id" integer NOT NULL REFERENCES "exams_subject" ("subject_id") DEFERRABLE INITIALLY DEFERRED, "teacher_id" bigint NOT NULL REFERENCES "administrator_teacher" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: administrator_timetable
CREATE TABLE IF NOT EXISTS "administrator_timetable" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "day" varchar(10) NOT NULL, "start_time" time NOT NULL, "end_time" time NOT NULL, "grade_id" bigint NOT NULL REFERENCES "learners_grade" ("id") DEFERRABLE INITIALLY DEFERRED, "subject_id" integer NOT NULL REFERENCES "exams_subject" ("subject_id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO administrator_timetable (id, day, start_time, end_time, grade_id, subject_id) VALUES (1, 'Monday', '08:00:00', '08:40:00', 10, 1);
INSERT INTO administrator_timetable (id, day, start_time, end_time, grade_id, subject_id) VALUES (3, 'Tuesday', '08:40:00', '09:20:00', 10, 2);

-- Table: auth_group
CREATE TABLE IF NOT EXISTS "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);

-- Table: auth_group_permissions
CREATE TABLE IF NOT EXISTS "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: auth_permission
CREATE TABLE IF NOT EXISTS "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (1, 1, 'add_logentry', 'Can add log entry');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (2, 1, 'change_logentry', 'Can change log entry');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (3, 1, 'delete_logentry', 'Can delete log entry');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (4, 1, 'view_logentry', 'Can view log entry');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (5, 2, 'add_permission', 'Can add permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (6, 2, 'change_permission', 'Can change permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (7, 2, 'delete_permission', 'Can delete permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (8, 2, 'view_permission', 'Can view permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (9, 3, 'add_group', 'Can add group');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (10, 3, 'change_group', 'Can change group');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (11, 3, 'delete_group', 'Can delete group');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (12, 3, 'view_group', 'Can view group');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (13, 4, 'add_user', 'Can add user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (14, 4, 'change_user', 'Can change user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (15, 4, 'delete_user', 'Can delete user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (16, 4, 'view_user', 'Can view user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (17, 5, 'add_contenttype', 'Can add content type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (18, 5, 'change_contenttype', 'Can change content type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (19, 5, 'delete_contenttype', 'Can delete content type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (20, 5, 'view_contenttype', 'Can view content type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (21, 6, 'add_session', 'Can add session');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (22, 6, 'change_session', 'Can change session');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (23, 6, 'delete_session', 'Can delete session');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (24, 6, 'view_session', 'Can view session');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (25, 7, 'add_learnermodel', 'Can add learner model');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (26, 7, 'change_learnermodel', 'Can change learner model');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (27, 7, 'delete_learnermodel', 'Can delete learner model');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (28, 7, 'view_learnermodel', 'Can view learner model');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (29, 8, 'add_learnerregister', 'Can add learner register');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (30, 8, 'change_learnerregister', 'Can change learner register');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (31, 8, 'delete_learnerregister', 'Can delete learner register');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (32, 8, 'view_learnerregister', 'Can view learner register');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (33, 9, 'add_feesmodel', 'Can add fees model');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (34, 9, 'change_feesmodel', 'Can change fees model');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (35, 9, 'delete_feesmodel', 'Can delete fees model');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (36, 9, 'view_feesmodel', 'Can view fees model');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (37, 10, 'add_examtype', 'Can add exam type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (38, 10, 'change_examtype', 'Can change exam type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (39, 10, 'delete_examtype', 'Can delete exam type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (40, 10, 'view_examtype', 'Can view exam type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (41, 11, 'add_subject', 'Can add subject');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (42, 11, 'change_subject', 'Can change subject');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (43, 11, 'delete_subject', 'Can delete subject');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (44, 11, 'view_subject', 'Can view subject');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (45, 12, 'add_examresult', 'Can add exam result');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (46, 12, 'change_examresult', 'Can change exam result');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (47, 12, 'delete_examresult', 'Can delete exam result');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (48, 12, 'view_examresult', 'Can view exam result');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (49, 13, 'add_learnertotalscore', 'Can add learner total score');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (50, 13, 'change_learnertotalscore', 'Can change learner total score');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (51, 13, 'delete_learnertotalscore', 'Can delete learner total score');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (52, 13, 'view_learnertotalscore', 'Can view learner total score');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (53, 14, 'add_grade', 'Can add grade');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (54, 14, 'change_grade', 'Can change grade');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (55, 14, 'delete_grade', 'Can delete grade');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (56, 14, 'view_grade', 'Can view grade');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (57, 15, 'add_school', 'Can add school');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (58, 15, 'change_school', 'Can change school');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (59, 15, 'delete_school', 'Can delete school');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (60, 15, 'view_school', 'Can view school');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (61, 19, 'add_academiccalendar', 'Can add academic calendar');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (62, 19, 'change_academiccalendar', 'Can change academic calendar');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (63, 19, 'delete_academiccalendar', 'Can delete academic calendar');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (64, 19, 'view_academiccalendar', 'Can view academic calendar');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (65, 20, 'add_attendance', 'Can add attendance');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (66, 20, 'change_attendance', 'Can change attendance');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (67, 20, 'delete_attendance', 'Can delete attendance');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (68, 20, 'view_attendance', 'Can view attendance');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (69, 21, 'add_teacher', 'Can add teacher');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (70, 21, 'change_teacher', 'Can change teacher');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (71, 21, 'delete_teacher', 'Can delete teacher');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (72, 21, 'view_teacher', 'Can view teacher');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (73, 22, 'add_teacherassignment', 'Can add teacher assignment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (74, 22, 'change_teacherassignment', 'Can change teacher assignment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (75, 22, 'delete_teacherassignment', 'Can delete teacher assignment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (76, 22, 'view_teacherassignment', 'Can view teacher assignment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (77, 23, 'add_timetable', 'Can add timetable');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (78, 23, 'change_timetable', 'Can change timetable');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (79, 23, 'delete_timetable', 'Can delete timetable');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (80, 23, 'view_timetable', 'Can view timetable');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (81, 24, 'add_curriculum', 'Can add curriculum');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (82, 24, 'change_curriculum', 'Can change curriculum');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (83, 24, 'delete_curriculum', 'Can delete curriculum');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (84, 24, 'view_curriculum', 'Can view curriculum');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (85, 16, 'add_role', 'Can add role');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (86, 16, 'change_role', 'Can change role');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (87, 16, 'delete_role', 'Can delete role');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (88, 16, 'view_role', 'Can view role');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (89, 17, 'add_custompermission', 'Can add custom permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (90, 17, 'change_custompermission', 'Can change custom permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (91, 17, 'delete_custompermission', 'Can delete custom permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (92, 17, 'view_custompermission', 'Can view custom permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (93, 18, 'add_customuser', 'Can add user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (94, 18, 'change_customuser', 'Can change user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (95, 18, 'delete_customuser', 'Can delete user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (96, 18, 'view_customuser', 'Can view user');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (97, 25, 'add_userprofile', 'Can add user profile');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (98, 25, 'change_userprofile', 'Can change user profile');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (99, 25, 'delete_userprofile', 'Can delete user profile');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (100, 25, 'view_userprofile', 'Can view user profile');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (101, 26, 'add_rolepermission', 'Can add role permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (102, 26, 'change_rolepermission', 'Can change role permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (103, 26, 'delete_rolepermission', 'Can delete role permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (104, 26, 'view_rolepermission', 'Can view role permission');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (105, 27, 'add_behavioralassessment', 'Can add behavioral assessment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (106, 27, 'change_behavioralassessment', 'Can change behavioral assessment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (107, 27, 'delete_behavioralassessment', 'Can delete behavioral assessment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (108, 27, 'view_behavioralassessment', 'Can view behavioral assessment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (109, 28, 'add_extracurricularactivity', 'Can add extra curricular activity');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (110, 28, 'change_extracurricularactivity', 'Can change extra curricular activity');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (111, 28, 'delete_extracurricularactivity', 'Can delete extra curricular activity');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (112, 28, 'view_extracurricularactivity', 'Can view extra curricular activity');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (113, 29, 'add_learninggoal', 'Can add learning goal');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (114, 29, 'change_learninggoal', 'Can change learning goal');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (115, 29, 'delete_learninggoal', 'Can delete learning goal');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (116, 29, 'view_learninggoal', 'Can view learning goal');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (117, 30, 'add_skillsassessment', 'Can add skills assessment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (118, 30, 'change_skillsassessment', 'Can change skills assessment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (119, 30, 'delete_skillsassessment', 'Can delete skills assessment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (120, 30, 'view_skillsassessment', 'Can view skills assessment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (121, 31, 'add_socialemotionaldevelopment', 'Can add social emotional development');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (122, 31, 'change_socialemotionaldevelopment', 'Can change social emotional development');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (123, 31, 'delete_socialemotionaldevelopment', 'Can delete social emotional development');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (124, 31, 'view_socialemotionaldevelopment', 'Can view social emotional development');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (125, 32, 'add_specialachievement', 'Can add special achievement');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (126, 32, 'change_specialachievement', 'Can change special achievement');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (127, 32, 'delete_specialachievement', 'Can delete special achievement');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (128, 32, 'view_specialachievement', 'Can view special achievement');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (129, 33, 'add_standardizedtestscore', 'Can add standardized test score');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (130, 33, 'change_standardizedtestscore', 'Can change standardized test score');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (131, 33, 'delete_standardizedtestscore', 'Can delete standardized test score');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (132, 33, 'view_standardizedtestscore', 'Can view standardized test score');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (133, 34, 'add_studyhabit', 'Can add study habit');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (134, 34, 'change_studyhabit', 'Can change study habit');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (135, 34, 'delete_studyhabit', 'Can delete study habit');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (136, 34, 'view_studyhabit', 'Can view study habit');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (137, 35, 'add_supportservice', 'Can add support service');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (138, 35, 'change_supportservice', 'Can change support service');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (139, 35, 'delete_supportservice', 'Can delete support service');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (140, 35, 'view_supportservice', 'Can view support service');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (141, 36, 'add_teachercomment', 'Can add teacher comment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (142, 36, 'change_teachercomment', 'Can change teacher comment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (143, 36, 'delete_teachercomment', 'Can delete teacher comment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (144, 36, 'view_teachercomment', 'Can view teacher comment');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (145, 37, 'add_attendance', 'Can add attendance');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (146, 37, 'change_attendance', 'Can change attendance');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (147, 37, 'delete_attendance', 'Can delete attendance');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (148, 37, 'view_attendance', 'Can view attendance');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (149, 38, 'add_progressreport', 'Can add progress report');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (150, 38, 'change_progressreport', 'Can change progress report');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (151, 38, 'delete_progressreport', 'Can delete progress report');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (152, 38, 'view_progressreport', 'Can view progress report');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (153, 39, 'add_classlevel', 'Can add class level');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (154, 39, 'change_classlevel', 'Can change class level');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (155, 39, 'delete_classlevel', 'Can delete class level');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (156, 39, 'view_classlevel', 'Can view class level');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (157, 40, 'add_feetype', 'Can add fee type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (158, 40, 'change_feetype', 'Can change fee type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (159, 40, 'delete_feetype', 'Can delete fee type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (160, 40, 'view_feetype', 'Can view fee type');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (161, 41, 'add_feerecord', 'Can add fee record');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (162, 41, 'change_feerecord', 'Can change fee record');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (163, 41, 'delete_feerecord', 'Can delete fee record');
INSERT INTO auth_permission (id, content_type_id, codename, name) VALUES (164, 41, 'view_feerecord', 'Can view fee record');

-- Table: auth_user
CREATE TABLE IF NOT EXISTS "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "first_name" varchar(150) NOT NULL);
INSERT INTO auth_user (id, password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name) VALUES (1, 'pbkdf2_sha256$720000$ZLqfHYTs23MIqgWYhKv2nM$VpCw2VKch5dwtiwU5IdLV7w/FJcUdLamU97L6V97kNs=', '2024-09-09 20:00:04.563862', 1, 'dkk', '', 'dkk@stmarys.com', 1, 1, '2024-09-06 17:20:36.778922', '');

-- Table: auth_user_groups
CREATE TABLE IF NOT EXISTS "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: auth_user_user_permissions
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: authenticator_custompermission
CREATE TABLE IF NOT EXISTS authenticator_custompermission (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, name varchar (255) NOT NULL UNIQUE, codename varchar (100) NOT NULL UNIQUE, content_type_id integer NOT NULL REFERENCES django_content_type (id) DEFERRABLE INITIALLY DEFERRED);

-- Table: authenticator_customuser
CREATE TABLE IF NOT EXISTS authenticator_customuser (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, password varchar (128) NOT NULL, last_login datetime, is_superuser bool NOT NULL, username varchar (150) NOT NULL UNIQUE, first_name varchar (150) NOT NULL, last_name varchar (150) NOT NULL, email varchar (254) NOT NULL, is_staff bool NOT NULL, is_active bool NOT NULL, date_joined datetime NOT NULL, user_type varchar (20) NOT NULL, role_id bigint REFERENCES authenticator_role (id) DEFERRABLE INITIALLY DEFERRED);
INSERT INTO authenticator_customuser (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, user_type, role_id) VALUES (1, 'pbkdf2_sha256$870000$SUIIRvNUARorzzDiFD9pCM$YjzJwHNrSdrKEk9QpDfRrVXuZ9RW9ooGCJOyF4tFfh0=', '2024-09-25 12:21:45.996623', 1, 'dkk', '', '', 'dkk@stmarys.com', 1, 1, '2024-09-11 14:07:31.521849', 'student', NULL);
INSERT INTO authenticator_customuser (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, user_type, role_id) VALUES (2, 'pbkdf2_sha256$870000$a2ogUBBvySqA963srU2P1y$g0YTuRc/LTtorQ7jq5GgWJLqg6zePszMC2SFMZhHxo8=', NULL, 1, 'sally', '', '', 'mugesally2020@gmail.com', 1, 1, '2024-09-25 07:34:22.495575', 'student', NULL);
INSERT INTO authenticator_customuser (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, user_type, role_id) VALUES (3, 'pbkdf2_sha256$870000$i4dAJGpKVsUTss0uMtj1dP$OdVgXBBIMB/we0VbspfXg2BAw1AwuVCAjf6d8RiIRcI=', NULL, 1, 'tarus', '', '', 'taruspeter1154@gmail.com', 1, 1, '2024-09-25 08:48:10.036613', 'student', NULL);
INSERT INTO authenticator_customuser (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, user_type, role_id) VALUES (4, 'pbkdf2_sha256$870000$LBTevZOuc4wTSPnkRr61TV$XQ/RbqSYNckN4hvZcTaW59WQEdmv4c7qLu0TG8f28Mo=', '2024-09-25 12:28:10.188997', 1, 'asbel', '', '', 'asbelronix@gmail.com', 1, 1, '2024-09-25 10:24:24.863316', 'student', NULL);

-- Table: authenticator_customuser_custom_permissions
CREATE TABLE IF NOT EXISTS authenticator_customuser_custom_permissions (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, customuser_id bigint NOT NULL REFERENCES authenticator_customuser (id) DEFERRABLE INITIALLY DEFERRED, custompermission_id bigint NOT NULL REFERENCES authenticator_custompermission (id) DEFERRABLE INITIALLY DEFERRED);

-- Table: authenticator_customuser_groups
CREATE TABLE IF NOT EXISTS authenticator_customuser_groups (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, customuser_id bigint NOT NULL REFERENCES authenticator_customuser (id) DEFERRABLE INITIALLY DEFERRED, group_id integer NOT NULL REFERENCES auth_group (id) DEFERRABLE INITIALLY DEFERRED);

-- Table: authenticator_customuser_user_permissions
CREATE TABLE IF NOT EXISTS authenticator_customuser_user_permissions (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, customuser_id bigint NOT NULL REFERENCES authenticator_customuser (id) DEFERRABLE INITIALLY DEFERRED, permission_id integer NOT NULL REFERENCES auth_permission (id) DEFERRABLE INITIALLY DEFERRED);

-- Table: authenticator_role
CREATE TABLE IF NOT EXISTS authenticator_role (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, name varchar (100) NOT NULL UNIQUE, description text NOT NULL);

-- Table: authenticator_rolepermission
CREATE TABLE IF NOT EXISTS authenticator_rolepermission (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, permission_id bigint NOT NULL REFERENCES authenticator_custompermission (id) DEFERRABLE INITIALLY DEFERRED, role_id bigint NOT NULL REFERENCES authenticator_role (id) DEFERRABLE INITIALLY DEFERRED);

-- Table: authenticator_userprofile
CREATE TABLE IF NOT EXISTS authenticator_userprofile (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, bio text NOT NULL, date_of_birth date, profile_picture varchar (100), user_id bigint NOT NULL UNIQUE REFERENCES authenticator_customuser (id) DEFERRABLE INITIALLY DEFERRED);

-- Table: django_admin_log
CREATE TABLE IF NOT EXISTS "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (1, '1', 'LearnerRegister object (1)', 1, '[{"added": {}}]', 8, 1, '2024-09-06 17:35:19.644470');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (2, '1', 'LearnerRegister object (1)', 2, '[{"changed": {"fields": ["Learner id"]}}]', 8, 1, '2024-09-06 17:39:59.314341');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (3, '1', 'FeesModel object (1)', 1, '[{"added": {}}]', 9, 1, '2024-09-06 17:42:13.620974');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (4, '2', '2407 mark      kipkoech', 1, '[{"added": {}}]', 8, 1, '2024-09-06 18:10:41.342466');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (5, '3', '2417 DISMAS  KIPKIRUI', 1, '[{"added": {}}]', 8, 1, '2024-09-06 18:14:29.226098');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (6, '4', '2409 ALLAN      KIPLAGAT', 1, '[{"added": {}}]', 8, 1, '2024-09-06 18:18:01.182202');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (7, '5', '24180 NICHOLAS       CHERUIYOT', 1, '[{"added": {}}]', 8, 1, '2024-09-06 18:26:53.370440');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (8, '6', '2421 griffin      kirwa', 1, '[{"added": {}}]', 8, 1, '2024-09-06 18:30:02.799156');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (9, '7', '2422 EMMANUEL         KIBET', 1, '[{"added": {}}]', 8, 1, '2024-09-06 18:31:53.555038');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (10, '2', '5000 CHEQUE BURSAR 2407 mark      kipkoech', 1, '[{"added": {}}]', 9, 1, '2024-09-06 18:34:49.174393');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (11, '3', '5000 CHEQUE BURSAR 2417 DISMAS  KIPKIRUI', 1, '[{"added": {}}]', 9, 1, '2024-09-06 18:35:21.545923');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (12, '4', '5000 CHEQUE BURSAR 2407 mark      kipkoech', 1, '[{"added": {}}]', 9, 1, '2024-09-06 18:35:50.858790');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (13, '5', '5000 CHEQUE BURSAR 24180 NICHOLAS       CHERUIYOT', 1, '[{"added": {}}]', 9, 1, '2024-09-06 18:36:50.340127');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (14, '6', '5000 CHEQUE BURSAR 2422 EMMANUEL         KIBET', 1, '[{"added": {}}]', 9, 1, '2024-09-06 18:37:57.148237');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (15, '7', '5000 CHEQUE BURSAR 1 EMMANUEL KIPKOECH SOIMO', 1, '[{"added": {}}]', 9, 1, '2024-09-06 18:38:20.654841');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (16, '1', '2411 EMMANUEL KIPKOECH SOIMO', 2, '[{"changed": {"fields": ["Learner id"]}}]', 8, 1, '2024-09-06 18:41:59.133576');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (17, '2', '2407 MARK     KIPKOECH', 2, '[{"changed": {"fields": ["Name", "Gender"]}}]', 8, 1, '2024-09-06 18:43:48.065165');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (18, '6', '2421 griffin      kirwa', 2, '[]', 8, 1, '2024-09-06 18:44:25.498882');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (19, '8', '5000 CHEQUE BURSAR 2411 EMMANUEL KIPKOECH SOIMO', 1, '[{"added": {}}]', 9, 1, '2024-09-06 18:45:50.041872');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (20, '9', '5000 CHEQUE BURSAR 2421 griffin      kirwa', 1, '[{"added": {}}]', 9, 1, '2024-09-06 18:46:39.116053');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (21, '6', '2421 GRIFFIN    KIRWA', 2, '[{"changed": {"fields": ["Name"]}}]', 8, 1, '2024-09-06 18:48:03.419890');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (22, '5', '2418 NICHOLAS       CHERUIYOT Parent 2024-03-11 MALE Contact', 2, '[{"changed": {"fields": ["Learner id"]}}]', 8, 1, '2024-09-07 08:50:59.692197');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (23, '1', 'JESMA 006, 2024-09-07, 1', 1, '[{"added": {}}]', 10, 1, '2024-09-07 08:59:52.740518');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (24, '1', 'MATHS, 1', 1, '[{"added": {}}]', 11, 1, '2024-09-07 09:02:42.961137');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (25, '2', 'SCIENCE, 2', 1, '[{"added": {}}]', 11, 1, '2024-09-07 09:02:46.489877');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (26, '3', 'SST, 3', 1, '[{"added": {}}]', 11, 1, '2024-09-07 09:02:48.847087');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (27, '4', 'CRE, 4', 1, '[{"added": {}}]', 11, 1, '2024-09-07 09:02:51.152827');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (28, '5', 'PRETECH, 5', 1, '[{"added": {}}]', 11, 1, '2024-09-07 09:02:54.050076');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (29, '6', 'KISWAHILI, 6', 1, '[{"added": {}}]', 11, 1, '2024-09-07 09:02:59.262252');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (30, '7', 'ENGLISH, 7', 1, '[{"added": {}}]', 11, 1, '2024-09-07 09:03:02.659077');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (31, '8', 'PHE, 8', 1, '[{"added": {}}]', 11, 1, '2024-09-07 09:03:05.548143');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (32, '9', 'CREATIVE ARTS, 9', 1, '[{"added": {}}]', 11, 1, '2024-09-07 09:03:28.051769');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (33, '8', '2401 MESHACK       KIPROTICH', 1, '[{"added": {}}]', 8, 1, '2024-09-07 09:07:48.076882');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (34, '10', '5000 CHEQUE BURSAR 2401 MESHACK       KIPROTICH', 1, '[{"added": {}}]', 9, 1, '2024-09-07 09:08:15.084282');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (35, '1', '2411 EMMANUEL KIPKOECH SOIMO, JESMA 006, 2024-09-07, 1, 78', 1, '[{"added": {}}]', 12, 1, '2024-09-07 09:24:38.267804');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (36, '1', '2411 EMMANUEL KIPKOECH SOIMO, JESMA 006, 2024-09-07, 1, 78.00', 3, '', 12, 1, '2024-09-07 09:24:58.828832');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (37, '1', '2411 EMMANUEL KIPKOECH SOIMO, JESMA 006, 2024-09-07, 1, 78.0, MATHS, 1, MATHS, 1', 1, '[{"added": {}}]', 12, 1, '2024-09-07 09:34:40.682504');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (38, '2', '2411 EMMANUEL KIPKOECH SOIMO, JESMA 006, 2024-09-07, 1, 70.0, SCIENCE, 2, SCIENCE, 2', 1, '[{"added": {}}]', 12, 1, '2024-09-07 09:34:51.894912');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (39, '1', '2411 EMMANUEL KIPKOECH SOIMO - MATHS, 1: 78.0', 1, '[{"added": {}}]', 12, 1, '2024-09-07 10:49:10.766646');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (40, '2', '2411 EMMANUEL KIPKOECH SOIMO - MATHS, 1: 88.0', 1, '[{"added": {}}]', 12, 1, '2024-09-07 10:49:36.851030');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (41, '2', '2411 EMMANUEL KIPKOECH SOIMO - MATHS, 1: 88.0', 3, '', 12, 1, '2024-09-07 10:49:48.111316');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (42, '1', '2411 EMMANUEL KIPKOECH SOIMO - MATHS, 1: 78.0', 2, '[{"changed": {"fields": ["Exam type"]}}]', 12, 1, '2024-09-07 17:18:58.544811');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (43, '3', '2401 MESHACK       KIPROTICH - MATHS, 1: 94.0', 1, '[{"added": {}}]', 12, 1, '2024-09-08 05:45:54.452001');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (44, '4', '2407 MARK     KIPKOECH - SST, 3: 62.0', 1, '[{"added": {}}]', 12, 1, '2024-09-08 05:48:41.554447');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (45, '5', '2417 DISMAS  KIPKIRUI - PRETECH, 5: 70.0', 1, '[{"added": {}}]', 12, 1, '2024-09-08 05:49:50.070713');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (46, '6', '2409 ALLAN      KIPLAGAT - SCIENCE, 2: 66.0', 1, '[{"added": {}}]', 12, 1, '2024-09-08 05:51:20.151142');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (47, '1', 'grade1', 1, '[{"added": {}}]', 14, 1, '2024-09-10 05:04:11.717705');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (48, '1', '2', 2, '[{"changed": {"fields": ["Grade name", "Grade description"]}}]', 14, 1, '2024-09-10 06:38:36.948898');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (49, '2', 'Pre-Primary-1', 1, '[{"added": {}}]', 14, 1, '2024-09-10 09:19:12.328189');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (50, '3', 'Pre-Primary-2', 1, '[{"added": {}}]', 14, 1, '2024-09-10 09:19:22.364545');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (51, '13', '2', 1, '[{"added": {}}]', 14, 1, '2024-09-10 10:01:42.004373');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (52, '12', '9', 2, '[{"changed": {"fields": ["Grade name"]}}]', 14, 1, '2024-09-10 10:04:12.792887');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (53, '4', '1', 2, '[{"changed": {"fields": ["Grade name"]}}]', 14, 1, '2024-09-10 10:04:26.813855');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (54, '11', '8', 2, '[{"changed": {"fields": ["Grade name"]}}]', 14, 1, '2024-09-10 10:04:42.534270');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (55, '10', '7', 2, '[{"changed": {"fields": ["Grade name"]}}]', 14, 1, '2024-09-10 10:04:49.814627');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (56, '9', '6', 2, '[{"changed": {"fields": ["Grade name"]}}]', 14, 1, '2024-09-10 10:05:10.706520');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (57, '8', '5', 2, '[{"changed": {"fields": ["Grade name"]}}]', 14, 1, '2024-09-10 10:05:17.767092');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (58, '7', '4', 2, '[{"changed": {"fields": ["Grade name"]}}]', 14, 1, '2024-09-10 10:05:25.446403');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (59, '6', '3', 2, '[{"changed": {"fields": ["Grade name"]}}]', 14, 1, '2024-09-10 10:05:33.113160');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (60, '9', '2424 Whole Numbers', 1, '[{"added": {}}]', 8, 1, '2024-09-10 17:29:39.593416');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (61, '10', '2426 Katalist LLC', 1, '[{"added": {}}]', 8, 1, '2024-09-10 17:29:57.375061');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (62, '11', '2427 PLPAfrica Web3', 1, '[{"added": {}}]', 8, 1, '2024-09-10 17:30:17.658856');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (63, '1', 'MATHS, 1', 2, '[{"changed": {"fields": ["Grades"]}}]', 11, 1, '2024-09-10 19:10:08.472115');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (64, '2', 'INT/SCI, 2', 2, '[{"changed": {"fields": ["Grades"]}}]', 11, 1, '2024-09-10 19:10:25.687056');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (65, '3', 'SST, 3', 2, '[{"changed": {"fields": ["Grades"]}}]', 11, 1, '2024-09-10 19:10:37.118577');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (66, '4', 'CRE, 4', 2, '[{"changed": {"fields": ["Grades"]}}]', 11, 1, '2024-09-10 19:10:47.132253');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (67, '5', 'PRE-TECH, 5', 2, '[{"changed": {"fields": ["Grades"]}}]', 11, 1, '2024-09-10 19:10:59.659104');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (68, '6', 'KISW, 6', 2, '[{"changed": {"fields": ["Grades"]}}]', 11, 1, '2024-09-10 19:11:08.625486');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (69, '7', 'ENG, 7', 2, '[{"changed": {"fields": ["Grades"]}}]', 11, 1, '2024-09-10 19:11:16.937510');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (70, '8', 'PHE, 8', 2, '[{"changed": {"fields": ["Grades"]}}]', 11, 1, '2024-09-10 19:11:38.490896');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (71, '9', 'C/ARTS, 9', 2, '[{"changed": {"fields": ["Grades"]}}]', 11, 1, '2024-09-10 19:19:14.036492');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (72, '2', '2407 MARK     KIPKOECH', 2, '[{"changed": {"fields": ["Fee balance", "Maize balance", "Beans balance"]}}]', 8, 1, '2024-09-10 21:08:08.683462');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (73, '12', '1001 Test Student', 1, '[{"added": {}}]', 8, 1, '2024-09-10 21:36:15.677943');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (74, '11', '2427 PLPAfrica Web3', 3, '', 8, 1, '2024-09-11 10:36:38.916910');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (75, '12', '1001 Test Student', 3, '', 8, 1, '2024-09-11 10:36:58.601594');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (76, '10', '2426 Katalist LLC', 3, '', 8, 1, '2024-09-11 10:36:58.620801');
INSERT INTO django_admin_log (id, object_id, object_repr, action_flag, change_message, content_type_id, user_id, action_time) VALUES (77, '9', '2424 Whole Numbers', 3, '', 8, 1, '2024-09-11 10:36:58.642469');

-- Table: django_content_type
CREATE TABLE IF NOT EXISTS "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
INSERT INTO django_content_type (id, app_label, model) VALUES (1, 'admin', 'logentry');
INSERT INTO django_content_type (id, app_label, model) VALUES (2, 'auth', 'permission');
INSERT INTO django_content_type (id, app_label, model) VALUES (3, 'auth', 'group');
INSERT INTO django_content_type (id, app_label, model) VALUES (4, 'auth', 'user');
INSERT INTO django_content_type (id, app_label, model) VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO django_content_type (id, app_label, model) VALUES (6, 'sessions', 'session');
INSERT INTO django_content_type (id, app_label, model) VALUES (7, 'learners', 'learnermodel');
INSERT INTO django_content_type (id, app_label, model) VALUES (8, 'learners', 'learnerregister');
INSERT INTO django_content_type (id, app_label, model) VALUES (9, 'learners', 'feesmodel');
INSERT INTO django_content_type (id, app_label, model) VALUES (10, 'exams', 'examtype');
INSERT INTO django_content_type (id, app_label, model) VALUES (11, 'exams', 'subject');
INSERT INTO django_content_type (id, app_label, model) VALUES (12, 'exams', 'examresult');
INSERT INTO django_content_type (id, app_label, model) VALUES (13, 'exams', 'learnertotalscore');
INSERT INTO django_content_type (id, app_label, model) VALUES (14, 'learners', 'grade');
INSERT INTO django_content_type (id, app_label, model) VALUES (15, 'learners', 'school');
INSERT INTO django_content_type (id, app_label, model) VALUES (16, 'authenticator', 'role');
INSERT INTO django_content_type (id, app_label, model) VALUES (17, 'authenticator', 'custompermission');
INSERT INTO django_content_type (id, app_label, model) VALUES (18, 'authenticator', 'customuser');
INSERT INTO django_content_type (id, app_label, model) VALUES (19, 'administrator', 'academiccalendar');
INSERT INTO django_content_type (id, app_label, model) VALUES (20, 'administrator', 'attendance');
INSERT INTO django_content_type (id, app_label, model) VALUES (21, 'administrator', 'teacher');
INSERT INTO django_content_type (id, app_label, model) VALUES (22, 'administrator', 'teacherassignment');
INSERT INTO django_content_type (id, app_label, model) VALUES (23, 'administrator', 'timetable');
INSERT INTO django_content_type (id, app_label, model) VALUES (24, 'administrator', 'curriculum');
INSERT INTO django_content_type (id, app_label, model) VALUES (25, 'authenticator', 'userprofile');
INSERT INTO django_content_type (id, app_label, model) VALUES (26, 'authenticator', 'rolepermission');
INSERT INTO django_content_type (id, app_label, model) VALUES (27, 'exams', 'behavioralassessment');
INSERT INTO django_content_type (id, app_label, model) VALUES (28, 'exams', 'extracurricularactivity');
INSERT INTO django_content_type (id, app_label, model) VALUES (29, 'exams', 'learninggoal');
INSERT INTO django_content_type (id, app_label, model) VALUES (30, 'exams', 'skillsassessment');
INSERT INTO django_content_type (id, app_label, model) VALUES (31, 'exams', 'socialemotionaldevelopment');
INSERT INTO django_content_type (id, app_label, model) VALUES (32, 'exams', 'specialachievement');
INSERT INTO django_content_type (id, app_label, model) VALUES (33, 'exams', 'standardizedtestscore');
INSERT INTO django_content_type (id, app_label, model) VALUES (34, 'exams', 'studyhabit');
INSERT INTO django_content_type (id, app_label, model) VALUES (35, 'exams', 'supportservice');
INSERT INTO django_content_type (id, app_label, model) VALUES (36, 'exams', 'teachercomment');
INSERT INTO django_content_type (id, app_label, model) VALUES (37, 'exams', 'attendance');
INSERT INTO django_content_type (id, app_label, model) VALUES (38, 'exams', 'progressreport');
INSERT INTO django_content_type (id, app_label, model) VALUES (39, 'learners', 'classlevel');
INSERT INTO django_content_type (id, app_label, model) VALUES (40, 'fees', 'feetype');
INSERT INTO django_content_type (id, app_label, model) VALUES (41, 'fees', 'feerecord');

-- Table: django_migrations
CREATE TABLE IF NOT EXISTS "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
INSERT INTO django_migrations (id, app, name, applied) VALUES (1, 'contenttypes', '0001_initial', '2024-09-06 17:19:39.589150');
INSERT INTO django_migrations (id, app, name, applied) VALUES (2, 'auth', '0001_initial', '2024-09-06 17:19:39.855368');
INSERT INTO django_migrations (id, app, name, applied) VALUES (3, 'admin', '0001_initial', '2024-09-06 17:19:40.044623');
INSERT INTO django_migrations (id, app, name, applied) VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2024-09-06 17:19:40.122453');
INSERT INTO django_migrations (id, app, name, applied) VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2024-09-06 17:19:40.232807');
INSERT INTO django_migrations (id, app, name, applied) VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2024-09-06 17:19:40.346727');
INSERT INTO django_migrations (id, app, name, applied) VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2024-09-06 17:19:40.494327');
INSERT INTO django_migrations (id, app, name, applied) VALUES (8, 'auth', '0003_alter_user_email_max_length', '2024-09-06 17:19:40.621976');
INSERT INTO django_migrations (id, app, name, applied) VALUES (9, 'auth', '0004_alter_user_username_opts', '2024-09-06 17:19:40.820485');
INSERT INTO django_migrations (id, app, name, applied) VALUES (10, 'auth', '0005_alter_user_last_login_null', '2024-09-06 17:19:40.937482');
INSERT INTO django_migrations (id, app, name, applied) VALUES (11, 'auth', '0006_require_contenttypes_0002', '2024-09-06 17:19:41.024969');
INSERT INTO django_migrations (id, app, name, applied) VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2024-09-06 17:19:41.119978');
INSERT INTO django_migrations (id, app, name, applied) VALUES (13, 'auth', '0008_alter_user_username_max_length', '2024-09-06 17:19:41.213675');
INSERT INTO django_migrations (id, app, name, applied) VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2024-09-06 17:19:41.317818');
INSERT INTO django_migrations (id, app, name, applied) VALUES (15, 'auth', '0010_alter_group_name_max_length', '2024-09-06 17:19:41.459784');
INSERT INTO django_migrations (id, app, name, applied) VALUES (16, 'auth', '0011_update_proxy_permissions', '2024-09-06 17:19:41.578740');
INSERT INTO django_migrations (id, app, name, applied) VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2024-09-06 17:19:41.700000');
INSERT INTO django_migrations (id, app, name, applied) VALUES (18, 'sessions', '0001_initial', '2024-09-06 17:19:41.891356');
INSERT INTO django_migrations (id, app, name, applied) VALUES (19, 'learners', '0001_initial', '2024-09-06 17:29:00.813485');
INSERT INTO django_migrations (id, app, name, applied) VALUES (20, 'learners', '0002_learnerregister_name_of_parent_and_more', '2024-09-06 17:34:18.100901');
INSERT INTO django_migrations (id, app, name, applied) VALUES (21, 'learners', '0003_learnerregister_learner_id_feesmodel', '2024-09-06 17:38:58.617374');
INSERT INTO django_migrations (id, app, name, applied) VALUES (22, 'learners', '0004_alter_feesmodel_learner_id_delete_learnermodel', '2024-09-06 17:41:32.918025');
INSERT INTO django_migrations (id, app, name, applied) VALUES (23, 'exams', '0001_initial', '2024-09-07 08:56:18.339885');
INSERT INTO django_migrations (id, app, name, applied) VALUES (24, 'exams', '0002_subject', '2024-09-07 09:01:36.745471');
INSERT INTO django_migrations (id, app, name, applied) VALUES (25, 'exams', '0003_examresult', '2024-09-07 09:24:13.572839');
INSERT INTO django_migrations (id, app, name, applied) VALUES (26, 'exams', '0004_remove_examresult_math_mark_examresult_score_and_more', '2024-09-07 09:33:55.927649');
INSERT INTO django_migrations (id, app, name, applied) VALUES (27, 'exams', '0005_alter_examresult_unique_together_and_more', '2024-09-07 10:44:30.315977');
INSERT INTO django_migrations (id, app, name, applied) VALUES (28, 'exams', '0004_remove_examresult_admission_number_and_more', '2024-09-07 10:49:04.607395');
INSERT INTO django_migrations (id, app, name, applied) VALUES (29, 'exams', '0005_learnertotalscore', '2024-09-07 11:15:21.033534');
INSERT INTO django_migrations (id, app, name, applied) VALUES (30, 'exams', '0006_alter_examresult_unique_together', '2024-09-07 17:12:57.934124');
INSERT INTO django_migrations (id, app, name, applied) VALUES (31, 'exams', '0007_examresult_exam_type', '2024-09-07 17:16:06.677412');
INSERT INTO django_migrations (id, app, name, applied) VALUES (32, 'learners', '0005_feesmodel_payment_method', '2024-09-09 18:59:18.004082');
INSERT INTO django_migrations (id, app, name, applied) VALUES (33, 'learners', '0006_learnerregister_grade_name', '2024-09-09 19:15:29.917536');
INSERT INTO django_migrations (id, app, name, applied) VALUES (34, 'learners', '0007_alter_learnerregister_grade_name', '2024-09-09 19:16:07.042649');
INSERT INTO django_migrations (id, app, name, applied) VALUES (35, 'learners', '0008_grade', '2024-09-09 19:58:28.016153');
INSERT INTO django_migrations (id, app, name, applied) VALUES (36, 'learners', '0009_feesmodel_payment_id', '2024-09-09 20:11:23.303603');
INSERT INTO django_migrations (id, app, name, applied) VALUES (37, 'learners', '0010_remove_learnerregister_grade_name_and_more', '2024-09-10 06:40:54.171600');
INSERT INTO django_migrations (id, app, name, applied) VALUES (38, 'learners', '0011_alter_grade_grade_name_alter_learnerregister_grade', '2024-09-10 06:40:54.198599');
INSERT INTO django_migrations (id, app, name, applied) VALUES (39, 'exams', '0008_alter_examresult_unique_together_and_more', '2024-09-10 06:40:54.372583');
INSERT INTO django_migrations (id, app, name, applied) VALUES (40, 'exams', '0009_alter_subject_grade', '2024-09-10 06:40:54.385585');
INSERT INTO django_migrations (id, app, name, applied) VALUES (41, 'learners', '0012_alter_grade_grade_name', '2024-09-10 10:09:18.865579');
INSERT INTO django_migrations (id, app, name, applied) VALUES (42, 'exams', '0010_remove_subject_grade_subject_grades', '2024-09-10 19:08:53.079122');
INSERT INTO django_migrations (id, app, name, applied) VALUES (43, 'exams', '0011_examresult_teacher_comment', '2024-09-10 20:33:49.737664');
INSERT INTO django_migrations (id, app, name, applied) VALUES (44, 'learners', '0013_school_grade_class_teacher_remark_and_more', '2024-09-10 20:33:49.865866');
INSERT INTO django_migrations (id, app, name, applied) VALUES (45, 'exams', '0012_examtype_term', '2024-09-11 08:25:33.920633');
INSERT INTO django_migrations (id, app, name, applied) VALUES (46, 'authenticator', '0001_initial', '2024-09-11 13:35:03.551321');
INSERT INTO django_migrations (id, app, name, applied) VALUES (47, 'administrator', '0001_initial', '2024-09-12 08:02:44.275397');
INSERT INTO django_migrations (id, app, name, applied) VALUES (48, 'administrator', '0002_remove_attendance_grade_remove_attendance_is_present_and_more', '2024-09-12 12:00:10.810685');
INSERT INTO django_migrations (id, app, name, applied) VALUES (49, 'exams', '0002_behavioralassessment_extracurricularactivity_and_more', '2024-09-12 12:00:11.141147');
INSERT INTO django_migrations (id, app, name, applied) VALUES (50, 'administrator', '0003_remove_teacher_contact_number_teacher_address_and_more', '2024-09-14 13:49:27.672079');
INSERT INTO django_migrations (id, app, name, applied) VALUES (51, 'learners', '0002_alter_learnerregister_gender_classlevel', '2024-09-14 13:49:27.809023');
INSERT INTO django_migrations (id, app, name, applied) VALUES (52, 'fees', '0001_initial', '2024-09-24 22:40:09.189789');

-- Table: django_session
CREATE TABLE IF NOT EXISTS "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('no3itvcrt8lcsns6e0ljcy7fj3ep0ame', '.eJxVjEEOwiAQRe_C2pACHQZcuvcMZOiAVA0kpV0Z765NutDtf-_9lwi0rSVsPS1hZnEWSpx-t0jTI9Ud8J3qrcmp1XWZo9wVedAur43T83K4fweFevnWyWDUGjEjOcxm0NZbNYD32ZtoKTogcjCOxMDKkmNDGtBky-icBy3eH8VzNwQ:1smzn0:PrXli8fl77APOcxoZVSGx4gYZRkVZnd79P75jL4162I', '2024-09-21 18:04:02.159109');
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('i8i8wxs5dhxqgn2832aomykd2ifl3i9p', '.eJxVjEEOwiAQRe_C2pACHQZcuvcMZOiAVA0kpV0Z765NutDtf-_9lwi0rSVsPS1hZnEWSpx-t0jTI9Ud8J3qrcmp1XWZo9wVedAur43T83K4fweFevnWyWDUGjEjOcxm0NZbNYD32ZtoKTogcjCOxMDKkmNDGtBky-icBy3eH8VzNwQ:1smzrm:S9JE8FmI556P7dhBtRKILrsVdsqSX71csvg8alJigcg', '2024-09-21 18:08:58.998745');
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('9l614q2qt8xuic2ennxlafhsumwpym5r', 'e30:1soOyu:sioSr-njT69pOUcqsA34hoiiYqwFNGosJ4FtTIeyO0k', '2024-09-25 15:10:08.874568');
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('p7p8aeuww5wxm8ocrxeg4c4vm60j3w7j', 'e30:1soOzU:1Om_WL1hJcYXCMRylWO7DzNwBmgWJfSR7YSob3Ka5RY', '2024-09-25 15:10:44.040058');
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('u53svnlxr05a96fyu5ct1sfowgv2vv1y', 'e30:1soP0F:r8YRWEBXAv0n_XLq-W17C3hOXlgMoJSPHhmGv9kIDls', '2024-09-25 15:11:31.302843');
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('dfyr4b9vd5l2e66ddjmxof9rouu3rlwk', 'e30:1soP7F:6NMm7eLgTLGOaIeRQamptmEPiJ_JXJtGZSNbaGFtMN4', '2024-09-25 15:18:45.391251');
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('qos77tyszkwrt9aljpzcg9jbb6qxyyzc', '.eJxVjEEOwiAQRe_C2hCgE3BcuvcMZBgYqRqalHbVeHdt0oVu_3vvbyrSutS49jLHMauLsur0uyXiZ2k7yA9q90nz1JZ5THpX9EG7vk25vK6H-3dQqddvDcKEAt6yJ2tDsOjyOQA5BE-C7FlEzAABc2YylIoZbADwqWByhOr9Ael1ODg:1sonFc:WyRcrU7Y0dy8dj5wqJr8ipiYsJubc_8OQm3jIxnJb_s', '2024-09-26 17:05:00.815738');
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('be8qu37y73t8zj89abpugjw28mmr3wl6', '.eJxVjEEOwiAQRe_C2hCgE3BcuvcMZBgYqRqalHbVeHdt0oVu_3vvbyrSutS49jLHMauLsur0uyXiZ2k7yA9q90nz1JZ5THpX9EG7vk25vK6H-3dQqddvDcKEAt6yJ2tDsOjyOQA5BE-C7FlEzAABc2YylIoZbADwqWByhOr9Ael1ODg:1st3zU:9gafaxvCPV51MGNyhZV-f0nnwfcUHD0JN1_uAr3ygbU', '2024-10-08 11:46:00.137273');
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('jhhj24dl8uh6ditio1d9268y05u4g3lq', '.eJxVjEEOwiAQRe_C2hCgE3BcuvcMZBgYqRqalHbVeHdt0oVu_3vvbyrSutS49jLHMauLsur0uyXiZ2k7yA9q90nz1JZ5THpX9EG7vk25vK6H-3dQqddvDcKEAt6yJ2tDsOjyOQA5BE-C7FlEzAABc2YylIoZbADwqWByhOr9Ael1ODg:1st4H0:RMDl-R1QFu0z-xqE5VvHNiaWEYdalYMl441GBvfGnXs', '2024-10-08 12:04:06.559511');
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('s8svr745njtfqq16u6es93zm3xw8ptur', '.eJxVjEsOwjAMBe-SNYrsOA6EJXvOUCWOSwoolfpZIe4OlbqA7ZuZ9zJdWpfarbNO3VDM2aA5_G45yUPbBso9tdtoZWzLNGS7KXans72ORZ-X3f07qGmu31qE1OeoIMeE6vpApyAuIvaMjJkhECAhJkEHnkkhkvMMDOSZSzHvD8nJNlQ:1stBdq:4IKIExDdfNIAp9_MX296ZJ1sD6p2sfBgxmMybXp6iDk', '2024-10-08 19:56:10.277419');
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('3j388a6hd9sp05d2u0qhh3urbs7uutrt', '.eJxVjEsOwjAMBe-SNYrs1KkxS_acoXISQwuokfpZIe4OlbqA7ZuZ93KdrkvfrbNN3VDcyZE7_G5J88PGDZS7jrfqcx2XaUh-U_xOZ3-pxZ7n3f076HXuv7WRMQaKlMk0YntVLqChCYZ8BBQSNgFpuTHJLDECJMIGMKqhQHLvD79-Nn8:1stQxi:3fkBwp3aCQ0OMN86lvfBKejs6pvn079ff1HpmrYUvco', '2024-10-09 12:17:42.924065');
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('0rq56armat8nx4zaxiknz0688wo1k3mx', '.eJxVjEsOwjAMBe-SNYrsOA6EJXvOUCWOSwoolfpZIe4OlbqA7ZuZ9zJdWpfarbNO3VDM2aA5_G45yUPbBso9tdtoZWzLNGS7KXans72ORZ-X3f07qGmu31qE1OeoIMeE6vpApyAuIvaMjJkhECAhJkEHnkkhkvMMDOSZSzHvD8nJNlQ:1stR1e:mVMf-kX2QLrv6FoVHsJveOJucDeyx28r1wIyYgHgSkc', '2024-10-09 12:21:46.004490');
INSERT INTO django_session (session_key, session_data, expire_date) VALUES ('kpki4g0f4gz6vlivxl5l5t8pofc3zxgx', '.eJxVjEsOwjAMBe-SNYrs1KkxS_acoXISQwuokfpZIe4OlbqA7ZuZ93KdrkvfrbNN3VDcyZE7_G5J88PGDZS7jrfqcx2XaUh-U_xOZ3-pxZ7n3f076HXuv7WRMQaKlMk0YntVLqChCYZ8BBQSNgFpuTHJLDECJMIGMKqhQHLvD79-Nn8:1stR7q:v_LpNCT_dHG3EQnWvVHEaBnykMUL_nFP5Uen1dyTkGY', '2024-10-09 12:28:10.197975');

-- Table: exams_attendance
CREATE TABLE IF NOT EXISTS "exams_attendance" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" date NOT NULL, "status" varchar(10) NOT NULL, "learner_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: exams_behavioralassessment
CREATE TABLE IF NOT EXISTS "exams_behavioralassessment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "category" varchar(50) NOT NULL, "rating" varchar(20) NOT NULL, "comment" text NOT NULL, "exam_type_id" integer NOT NULL REFERENCES "exams_examtype" ("exam_id") DEFERRABLE INITIALLY DEFERRED, "learner_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: exams_examresult
CREATE TABLE IF NOT EXISTS "exams_examresult" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date_examined" date NULL, "learner_id_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED, "score" real NULL, "subject_id" integer NOT NULL REFERENCES "exams_subject" ("subject_id") DEFERRABLE INITIALLY DEFERRED, "exam_type_id" integer NULL REFERENCES "exams_examtype" ("exam_id") DEFERRABLE INITIALLY DEFERRED, "teacher_comment" text NOT NULL);
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (79, '2024-09-24', 228, 57.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (80, '2024-09-24', 236, 66.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (81, '2024-09-24', 229, 60.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (82, '2024-09-24', 230, 64.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (83, '2024-09-24', 231, 57.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (84, '2024-09-24', 232, 53.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (85, '2024-09-24', 233, 56.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (86, '2024-09-24', 234, 57.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (87, '2024-09-24', 235, 46.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (88, '2024-09-24', 237, 40.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (89, '2024-09-24', 238, 40.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (90, '2024-09-24', 239, 46.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (91, '2024-09-24', 240, 46.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (92, '2024-09-24', 241, 43.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (93, '2024-09-24', 242, 36.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (94, '2024-09-24', 243, 56.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (95, '2024-09-24', 244, 30.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (96, '2024-09-24', 245, 40.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (97, '2024-09-24', 246, 36.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (98, '2024-09-24', 247, 46.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (99, '2024-09-24', 248, 43.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (100, '2024-09-24', 171, 72.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (101, '2024-09-24', 170, 86.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (102, '2024-09-24', 172, 67.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (103, '2024-09-24', 173, 76.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (104, '2024-09-24', 174, 72.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (105, '2024-09-24', 175, 72.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (106, '2024-09-24', 176, 56.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (107, '2024-09-24', 177, 64.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (108, '2024-09-24', 178, 56.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (109, '2024-09-24', 179, 69.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (110, '2024-09-24', 180, 69.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (111, '2024-09-24', 181, 60.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (112, '2024-09-24', 182, 70.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (113, '2024-09-24', 183, 76.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (114, '2024-09-24', 184, 60.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (115, '2024-09-24', 185, 76.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (116, '2024-09-24', 186, 76.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (117, '2024-09-24', 187, 69.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (118, '2024-09-24', 188, 53.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (119, '2024-09-24', 189, 72.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (120, '2024-09-24', 190, 64.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (121, '2024-09-24', 191, 46.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (122, '2024-09-24', 192, 46.0, 1, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (123, '2024-09-24', 228, 78.0, 4, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (124, '2024-09-24', 170, 76.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (125, '2024-09-24', 171, 60.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (126, '2024-09-24', 172, 60.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (127, '2024-09-24', 173, 73.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (128, '2024-09-24', 174, 60.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (129, '2024-09-24', 175, 57.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (130, '2024-09-24', 176, 60.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (131, '2024-09-24', 177, 70.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (132, '2024-09-24', 178, 63.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (133, '2024-09-24', 179, 60.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (134, '2024-09-24', 180, 63.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (135, '2024-09-24', 181, 53.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (136, '2024-09-24', 182, 53.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (137, '2024-09-24', 183, 57.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (138, '2024-09-24', 184, 60.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (139, '2024-09-24', 185, 30.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (140, '2024-09-24', 186, 70.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (141, '2024-09-24', 187, 33.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (142, '2024-09-24', 188, 43.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (143, '2024-09-24', 189, 43.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (144, '2024-09-24', 190, 50.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (145, '2024-09-24', 191, 30.0, 2, 4, '');
INSERT INTO exams_examresult (id, date_examined, learner_id_id, score, subject_id, exam_type_id, teacher_comment) VALUES (146, '2024-09-24', 192, 30.0, 2, 4, '');

-- Table: exams_examtype
CREATE TABLE IF NOT EXISTS "exams_examtype" ("name" varchar(100) NOT NULL, "date_administered" date NOT NULL, "exam_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "term" varchar(100) NOT NULL);
INSERT INTO exams_examtype (name, date_administered, exam_id, term) VALUES ('MID TERM 3', '2024-09-24', 4, 'Term 3');

-- Table: exams_extracurricularactivity
CREATE TABLE IF NOT EXISTS "exams_extracurricularactivity" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "activity" varchar(100) NOT NULL, "role" varchar(50) NOT NULL, "achievement" text NULL, "exam_type_id" integer NOT NULL REFERENCES "exams_examtype" ("exam_id") DEFERRABLE INITIALLY DEFERRED, "learner_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: exams_learnertotalscore
CREATE TABLE IF NOT EXISTS "exams_learnertotalscore" ("learner_id" bigint NOT NULL PRIMARY KEY REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED, "total_score" real NOT NULL, "exam_type_id" integer NULL REFERENCES "exams_examtype" ("exam_id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (21, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (22, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (23, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (24, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (25, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (26, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (27, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (28, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (29, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (30, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (31, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (32, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (33, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (34, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (35, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (36, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (37, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (38, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (39, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (40, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (41, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (42, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (43, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (44, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (45, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (46, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (47, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (48, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (49, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (50, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (51, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (52, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (53, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (54, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (55, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (56, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (57, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (58, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (59, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (60, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (61, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (62, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (63, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (64, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (65, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (66, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (67, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (68, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (69, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (70, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (71, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (72, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (73, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (74, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (75, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (76, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (77, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (78, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (79, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (80, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (81, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (82, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (83, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (84, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (85, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (86, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (87, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (88, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (89, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (90, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (91, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (92, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (93, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (94, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (95, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (96, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (97, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (98, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (99, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (100, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (101, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (102, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (103, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (104, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (105, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (106, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (107, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (108, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (109, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (110, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (111, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (112, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (113, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (114, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (115, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (116, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (117, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (118, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (119, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (120, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (121, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (122, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (123, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (124, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (125, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (126, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (127, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (128, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (129, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (130, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (131, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (132, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (133, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (134, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (135, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (136, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (137, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (138, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (139, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (140, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (141, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (142, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (143, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (144, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (145, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (146, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (147, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (148, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (149, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (150, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (151, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (152, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (153, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (154, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (155, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (156, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (157, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (158, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (159, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (160, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (161, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (162, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (163, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (164, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (165, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (166, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (167, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (168, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (169, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (170, 86.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (171, 72.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (172, 67.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (173, 76.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (174, 72.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (175, 72.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (176, 56.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (177, 64.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (178, 56.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (179, 69.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (180, 69.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (181, 60.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (182, 70.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (183, 76.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (184, 60.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (185, 76.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (186, 76.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (187, 69.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (188, 53.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (189, 72.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (190, 64.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (191, 46.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (192, 46.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (193, 376.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (194, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (195, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (196, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (197, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (198, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (199, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (200, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (201, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (202, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (203, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (204, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (205, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (206, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (207, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (208, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (209, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (210, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (211, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (212, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (213, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (214, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (215, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (216, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (217, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (218, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (219, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (220, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (221, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (222, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (223, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (224, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (225, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (226, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (227, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (228, 57.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (229, 60.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (230, 64.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (231, 57.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (232, 53.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (233, 56.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (234, 57.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (235, 46.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (236, 66.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (237, 40.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (238, 40.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (239, 46.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (240, 46.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (241, 43.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (242, 36.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (243, 56.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (244, 30.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (245, 40.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (246, 36.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (247, 46.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (248, 43.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (249, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (250, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (251, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (252, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (253, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (254, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (255, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (256, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (257, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (258, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (259, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (260, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (261, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (262, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (263, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (264, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (265, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (266, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (267, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (268, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (269, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (270, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (271, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (272, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (273, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (274, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (275, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (276, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (277, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (278, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (279, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (280, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (281, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (282, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (283, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (284, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (285, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (286, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (287, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (288, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (289, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (290, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (291, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (292, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (293, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (294, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (295, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (296, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (297, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (298, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (299, 0.0, 4);
INSERT INTO exams_learnertotalscore (learner_id, total_score, exam_type_id) VALUES (300, 0.0, 4);

-- Table: exams_learninggoal
CREATE TABLE IF NOT EXISTS "exams_learninggoal" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "goal" text NOT NULL, "status" varchar(20) NOT NULL, "exam_type_id" integer NOT NULL REFERENCES "exams_examtype" ("exam_id") DEFERRABLE INITIALLY DEFERRED, "learner_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: exams_progressreport
CREATE TABLE IF NOT EXISTS "exams_progressreport" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "generated_date" date NOT NULL, "overall_comment" text NOT NULL, "areas_for_improvement" text NOT NULL, "future_recommendations" text NOT NULL, "principal_signature" bool NOT NULL, "parent_signature" bool NOT NULL, "exam_type_id" integer NOT NULL REFERENCES "exams_examtype" ("exam_id") DEFERRABLE INITIALLY DEFERRED, "learner_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: exams_skillsassessment
CREATE TABLE IF NOT EXISTS "exams_skillsassessment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "skill" varchar(50) NOT NULL, "rating" varchar(20) NOT NULL, "exam_type_id" integer NOT NULL REFERENCES "exams_examtype" ("exam_id") DEFERRABLE INITIALLY DEFERRED, "learner_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: exams_socialemotionaldevelopment
CREATE TABLE IF NOT EXISTS "exams_socialemotionaldevelopment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "category" varchar(50) NOT NULL, "rating" varchar(20) NOT NULL, "comment" text NOT NULL, "exam_type_id" integer NOT NULL REFERENCES "exams_examtype" ("exam_id") DEFERRABLE INITIALLY DEFERRED, "learner_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: exams_specialachievement
CREATE TABLE IF NOT EXISTS "exams_specialachievement" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "achievement" text NOT NULL, "date" date NOT NULL, "exam_type_id" integer NOT NULL REFERENCES "exams_examtype" ("exam_id") DEFERRABLE INITIALLY DEFERRED, "learner_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: exams_standardizedtestscore
CREATE TABLE IF NOT EXISTS "exams_standardizedtestscore" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "test_name" varchar(100) NOT NULL, "score" decimal NOT NULL, "date" date NOT NULL, "exam_type_id" integer NOT NULL REFERENCES "exams_examtype" ("exam_id") DEFERRABLE INITIALLY DEFERRED, "learner_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: exams_studyhabit
CREATE TABLE IF NOT EXISTS "exams_studyhabit" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "category" varchar(50) NOT NULL, "rating" varchar(20) NOT NULL, "comment" text NOT NULL, "exam_type_id" integer NOT NULL REFERENCES "exams_examtype" ("exam_id") DEFERRABLE INITIALLY DEFERRED, "learner_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: exams_subject
CREATE TABLE IF NOT EXISTS "exams_subject" ("name" varchar(100) NOT NULL, "subject_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT);
INSERT INTO exams_subject (name, subject_id) VALUES ('MATHS', 1);
INSERT INTO exams_subject (name, subject_id) VALUES ('INT/SCI', 2);
INSERT INTO exams_subject (name, subject_id) VALUES ('SST', 3);
INSERT INTO exams_subject (name, subject_id) VALUES ('CRE', 4);
INSERT INTO exams_subject (name, subject_id) VALUES ('PRE-TECH', 5);
INSERT INTO exams_subject (name, subject_id) VALUES ('KISW', 6);
INSERT INTO exams_subject (name, subject_id) VALUES ('ENG', 7);
INSERT INTO exams_subject (name, subject_id) VALUES ('PHE', 8);
INSERT INTO exams_subject (name, subject_id) VALUES ('C/ARTS', 9);
INSERT INTO exams_subject (name, subject_id) VALUES ('ENV', 13);
INSERT INTO exams_subject (name, subject_id) VALUES ('SOCIAL ARTS', 14);

-- Table: exams_subject_grades
CREATE TABLE IF NOT EXISTS "exams_subject_grades" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "subject_id" integer NOT NULL REFERENCES "exams_subject" ("subject_id") DEFERRABLE INITIALLY DEFERRED, "grade_id" bigint NOT NULL REFERENCES "learners_grade" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (1, 1, 1);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (2, 1, 3);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (3, 1, 4);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (4, 1, 5);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (5, 1, 6);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (6, 1, 7);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (7, 1, 8);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (8, 1, 9);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (10, 1, 11);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (11, 1, 12);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (13, 2, 11);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (14, 2, 12);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (16, 3, 11);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (17, 3, 12);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (18, 4, 1);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (19, 4, 3);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (20, 4, 4);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (21, 4, 5);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (22, 4, 6);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (25, 4, 9);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (27, 4, 11);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (28, 4, 12);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (30, 5, 11);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (31, 5, 12);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (32, 6, 1);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (33, 6, 3);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (34, 6, 4);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (35, 6, 5);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (36, 6, 6);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (37, 6, 7);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (38, 6, 8);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (39, 6, 9);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (41, 6, 11);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (42, 6, 12);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (43, 7, 1);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (44, 7, 3);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (45, 7, 4);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (46, 7, 5);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (47, 7, 6);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (48, 7, 7);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (49, 7, 8);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (50, 7, 9);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (52, 7, 11);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (53, 7, 12);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (56, 8, 9);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (58, 8, 11);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (59, 8, 12);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (61, 9, 11);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (62, 9, 12);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (64, 1, 10);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (65, 2, 10);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (66, 3, 10);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (67, 4, 10);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (68, 5, 10);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (69, 6, 10);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (70, 7, 10);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (71, 8, 10);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (72, 9, 10);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (73, 13, 4);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (74, 13, 5);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (75, 13, 6);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (76, 9, 4);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (77, 9, 5);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (78, 9, 6);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (79, 14, 8);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (80, 14, 7);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (81, 2, 8);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (82, 2, 9);
INSERT INTO exams_subject_grades (id, subject_id, grade_id) VALUES (83, 2, 7);

-- Table: exams_supportservice
CREATE TABLE IF NOT EXISTS "exams_supportservice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "service_type" varchar(50) NOT NULL, "description" text NOT NULL, "start_date" date NOT NULL, "end_date" date NULL, "exam_type_id" integer NOT NULL REFERENCES "exams_examtype" ("exam_id") DEFERRABLE INITIALLY DEFERRED, "learner_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: exams_teachercomment
CREATE TABLE IF NOT EXISTS "exams_teachercomment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "comment" text NOT NULL, "exam_type_id" integer NOT NULL REFERENCES "exams_examtype" ("exam_id") DEFERRABLE INITIALLY DEFERRED, "learner_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED, "subject_id" integer NULL REFERENCES "exams_subject" ("subject_id") DEFERRABLE INITIALLY DEFERRED, "teacher_id" bigint NOT NULL REFERENCES "authenticator_customuser" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: fees_feerecord
CREATE TABLE IF NOT EXISTS "fees_feerecord" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "amount" decimal NOT NULL, "due_date" date NOT NULL, "paid_amount" decimal NOT NULL, "paid_date" date NULL, "status" varchar(10) NOT NULL, "learner_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED, "fee_type_id" bigint NOT NULL REFERENCES "fees_feetype" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: fees_feetype
CREATE TABLE IF NOT EXISTS "fees_feetype" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "description" text NOT NULL);

-- Table: learners_classlevel
CREATE TABLE IF NOT EXISTS "learners_classlevel" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "level_name" varchar(100) NOT NULL UNIQUE, "level_description" text NOT NULL, "class_representative_female_id" bigint NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED, "class_representative_male_id" bigint NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED, "class_teacher_id" bigint NULL REFERENCES "administrator_teacher" ("id") DEFERRABLE INITIALLY DEFERRED);

-- Table: learners_feesmodel
CREATE TABLE IF NOT EXISTS "learners_feesmodel" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "register_date" datetime NOT NULL, "amount" integer NOT NULL, "payment_type" varchar(100) NOT NULL, "received_by" varchar(100) NOT NULL, "learner_id_id" bigint NOT NULL REFERENCES "learners_learnerregister" ("id") DEFERRABLE INITIALLY DEFERRED, "payment_method" varchar(20) NOT NULL, "payment_id" integer NOT NULL);

-- Table: learners_grade
CREATE TABLE IF NOT EXISTS "learners_grade" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "grade_name" varchar(100) NOT NULL UNIQUE, "grade_description" text NOT NULL, "class_teacher_remark" text NOT NULL);
INSERT INTO learners_grade (id, grade_name, grade_description, class_teacher_remark) VALUES (1, 'Pre-Primary-1', 'PrePrimary 1', '');
INSERT INTO learners_grade (id, grade_name, grade_description, class_teacher_remark) VALUES (3, 'Pre-Primary-2', 'PrePrimary 2', '');
INSERT INTO learners_grade (id, grade_name, grade_description, class_teacher_remark) VALUES (4, 'Grade 1', 'Grade 1', '');
INSERT INTO learners_grade (id, grade_name, grade_description, class_teacher_remark) VALUES (5, 'Grade 2', 'Grade 2', '');
INSERT INTO learners_grade (id, grade_name, grade_description, class_teacher_remark) VALUES (6, 'Grade 3', 'Grade 3', '');
INSERT INTO learners_grade (id, grade_name, grade_description, class_teacher_remark) VALUES (7, 'Grade 4', 'Grade 4', '');
INSERT INTO learners_grade (id, grade_name, grade_description, class_teacher_remark) VALUES (8, 'Grade 5', 'Grade 5', '');
INSERT INTO learners_grade (id, grade_name, grade_description, class_teacher_remark) VALUES (9, 'Grade 6', 'Grade 6', '');
INSERT INTO learners_grade (id, grade_name, grade_description, class_teacher_remark) VALUES (10, 'Grade 7', 'Grade 7', 'Good effort. Aim higher.');
INSERT INTO learners_grade (id, grade_name, grade_description, class_teacher_remark) VALUES (11, 'Grade 8', 'Grade 8', '');
INSERT INTO learners_grade (id, grade_name, grade_description, class_teacher_remark) VALUES (12, 'Grade 9', 'Grade 9', '');

-- Table: learners_learnerregister
CREATE TABLE IF NOT EXISTS "learners_learnerregister" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "register_date" datetime NOT NULL, "date_of_birth" date NOT NULL, "name" varchar(100) NOT NULL, "gender" varchar(100) NOT NULL, "name_of_parent" varchar(100) NOT NULL, "parent_contact" varchar(100) NOT NULL, "learner_id" integer NOT NULL UNIQUE, "grade_id" bigint NOT NULL REFERENCES "learners_grade" ("id") DEFERRABLE INITIALLY DEFERRED, "beans_balance" decimal NOT NULL, "fee_balance" decimal NOT NULL, "maize_balance" decimal NOT NULL);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (21, '2024-09-24 06:26:22.157046', '2021-01-01', 'MERCYLINE JEPKURUI', 'Female', 'Parent', '254701234567', 1234, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (22, '2024-09-24 06:26:22.185971', '2021-01-02', 'JAYDEN KIPKOECH', 'Male', 'Parent', '254701234567', 1235, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (23, '2024-09-24 06:26:22.213675', '2021-01-03', 'ADRIAN KIPRUTO', 'Male', 'Parent', '254701234567', 1236, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (24, '2024-09-24 06:26:22.230855', '2021-01-04', 'LAURYN CHEROTICH', 'Female', 'Parent', '254701234567', 1237, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (25, '2024-09-24 06:26:22.251891', '2021-01-05', 'JAYDEN KIPRUTO', 'Male', 'Parent', '254701234567', 1238, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (26, '2024-09-24 06:26:22.270625', '2021-01-06', 'NOLAN GREG NYAGUA', 'Male', 'Parent', '254701234567', 1239, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (27, '2024-09-24 06:26:22.291762', '2021-01-07', 'JEALIAN JEPNGETICH', 'Female', 'Parent', '254701234567', 1240, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (28, '2024-09-24 06:26:22.314344', '2021-01-08', 'NAREL CHESIRO', 'Female', 'Parent', '254701234567', 1241, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (29, '2024-09-24 06:26:22.334443', '2021-01-09', 'SHANTEL JEROP', 'Female', 'Parent', '254701234567', 1242, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (30, '2024-09-24 06:26:22.355143', '2021-01-10', 'NOELA CHEBET', 'Female', 'Parent', '254701234567', 1243, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (31, '2024-09-24 06:26:22.374672', '2021-01-11', 'DENZEL KIMUTAI', 'Male', 'Parent', '254701234567', 1244, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (32, '2024-09-24 06:26:22.394865', '2021-01-12', 'IGNATIUS KIGEN', 'Male', 'Parent', '254701234567', 1245, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (33, '2024-09-24 06:26:22.412590', '2021-01-13', 'RAPHAEL KIPTANUI', 'Male', 'Parent', '254701234567', 1246, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (34, '2024-09-24 06:26:22.434707', '2021-01-14', 'EMMANUEL KIRWA', 'Male', 'Parent', '254701234567', 1247, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (35, '2024-09-24 06:26:22.452613', '2021-01-15', 'JAREL KECHA', 'Male', 'Parent', '254701234567', 1248, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (36, '2024-09-24 06:26:22.472479', '2021-01-16', 'AINOAM JELAGAT', 'Female', 'Parent', '254701234567', 1249, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (37, '2024-09-24 06:26:22.489356', '2021-01-17', 'LEXI JEMUTAI', 'Female', 'Parent', '254701234567', 1250, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (38, '2024-09-24 06:26:22.506823', '2021-01-18', 'PRECIOUS JEPKEMBOI', 'Female', 'Parent', '254701234567', 1251, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (39, '2024-09-24 06:26:22.528369', '2021-01-19', 'JAYDEN KIPKOSGEI', 'Male', 'Parent', '254701234567', 1252, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (40, '2024-09-24 06:26:22.544558', '2021-01-20', 'GODIOUS KIPTOO', 'Male', 'Parent', '254701234567', 1253, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (41, '2024-09-24 06:26:22.560420', '2021-01-21', 'ADELLE QUEEN JERUTO', 'Female', 'Parent', '254701234567', 1254, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (42, '2024-09-24 06:26:22.579409', '2021-01-22', 'BRAIDEN KIPKOECH', 'Male', 'Parent', '254701234567', 1255, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (43, '2024-09-24 06:26:22.597690', '2021-01-23', 'LYNE JEPTOO', 'Female', 'Parent', '254701234567', 1256, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (44, '2024-09-24 06:26:22.614898', '2021-01-24', 'RAVIANNI KIGEN ', 'Male', 'Parent', '254701234567', 1257, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (45, '2024-09-24 06:26:22.632349', '2021-01-25', 'APHAXARD KIGEN', 'Male', 'Parent', '254701234567', 1258, 1, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (46, '2024-09-24 06:29:40.032108', '2021-01-01', 'CALVIN KIPTOO', 'Female', 'Parent', '254701234567', 1301, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (47, '2024-09-24 06:29:40.048111', '2021-01-02', 'SHALINE JERUTO', 'Female', 'Parent', '254701234567', 1302, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (48, '2024-09-24 06:29:40.054630', '2021-01-03', 'BLESSING JEPCHUMBA', 'Female', 'Parent', '254701234567', 1303, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (49, '2024-09-24 06:29:40.063746', '2021-01-04', 'MARLON KIMURGOR', 'Male', 'Parent', '254701234567', 1304, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (50, '2024-09-24 06:29:40.071389', '2021-01-05', 'ABIGAEL JEPKOGEI', 'Female', 'Parent', '254701234567', 1305, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (51, '2024-09-24 06:29:40.081326', '2021-01-06', 'JOY JEPCHUMBA', 'Female', 'Parent', '254701234567', 1306, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (52, '2024-09-24 06:29:40.089614', '2021-01-07', 'RODGERS KIPTOO', 'Male', 'Parent', '254701234567', 1307, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (53, '2024-09-24 06:29:40.101738', '2021-01-08', 'RAYN KIPKOGEI', 'Male', 'Parent', '254701234567', 1308, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (54, '2024-09-24 06:29:40.110754', '2021-01-09', 'JAYDEN KIPKEMBOI', 'Male', 'Parent', '254701234567', 1309, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (55, '2024-09-24 06:29:40.119501', '2021-01-10', 'DALINE JERONO', 'Female', 'Parent', '254701234567', 1310, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (56, '2024-09-24 06:29:40.128726', '2021-01-11', 'NICOLEL JEROP', 'Female', 'Parent', '254701234567', 1311, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (57, '2024-09-24 06:29:40.137159', '2021-01-12', 'SHAMEL JEPLETING', 'Female', 'Parent', '254701234567', 1312, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (58, '2024-09-24 06:29:40.147638', '2021-01-13', 'SHAMY JEPKOGEI', 'Female', 'Parent', '254701234567', 1313, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (59, '2024-09-24 06:29:40.154710', '2021-01-14', 'ADRIEL KIPRUTO', 'Male', 'Parent', '254701234567', 1314, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (60, '2024-09-24 06:29:40.163257', '2021-01-15', 'IAN KIPKEMBOI', 'Male', 'Parent', '254701234567', 1315, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (61, '2024-09-24 06:29:40.174406', '2021-01-16', 'EDGAR KIPCHIRCHIR ', 'Male', 'Parent', '254701234567', 1316, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (62, '2024-09-24 06:29:40.193419', '2021-01-17', 'ATHALIAH JEMELI', 'Female', 'Parent', '254701234567', 1317, 3, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (63, '2024-09-24 06:32:51.882985', '2021-01-01', 'IGINITIOUS KIBET', 'Male', 'Parent', '254701234567', 1401, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (64, '2024-09-24 06:32:51.893952', '2021-01-02', 'SHANTEL CHEROTICH', 'Female', 'Parent', '254701234567', 1402, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (65, '2024-09-24 06:32:51.900869', '2021-01-03', 'TALIA CHEBET', 'Female', 'Parent', '254701234567', 1403, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (66, '2024-09-24 06:32:51.910243', '2021-01-04', 'SANDRA JEPTOO', 'Female', 'Parent', '254701234567', 1404, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (67, '2024-09-24 06:32:51.917234', '2021-01-05', 'BLESSINGS JEPKOECH', 'Female', 'Parent', '254701234567', 1405, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (68, '2024-09-24 06:32:51.924336', '2021-01-06', 'NICOLE JEPKOECH', 'Female', 'Parent', '254701234567', 1406, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (69, '2024-09-24 06:32:51.932342', '2021-01-07', 'GENEVICIA JEROP', 'Female', 'Parent', '254701234567', 1407, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (70, '2024-09-24 06:32:51.938067', '2021-01-08', 'NICOLE JEPKOSGEI', 'Female', 'Parent', '254701234567', 1408, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (71, '2024-09-24 06:32:51.947851', '2021-01-09', 'ADRIAN KIPRUTO', 'Male', 'Parent', '254701234567', 1409, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (72, '2024-09-24 06:32:51.953857', '2021-01-10', 'CYDEN KIPLIMO', 'Male', 'Parent', '254701234567', 1410, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (73, '2024-09-24 06:32:51.962155', '2021-01-11', 'GODWIN KIBIWOTT', 'Male', 'Parent', '254701234567', 1411, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (74, '2024-09-24 06:32:51.968063', '2021-01-12', 'SHAWN KIPKOECH', 'Male', 'Parent', '254701234567', 1412, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (75, '2024-09-24 06:32:51.976734', '2021-01-13', 'ROBERT KIPCHUMBA', 'Male', 'Parent', '254701234567', 1413, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (76, '2024-09-24 06:32:51.984312', '2021-01-14', 'HILLARY KIPCHUMBA', 'Male', 'Parent', '254701234567', 1414, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (77, '2024-09-24 06:32:51.992012', '2021-01-15', 'LEWIS KIGEN', 'Male', 'Parent', '254701234567', 1415, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (78, '2024-09-24 06:32:51.999699', '2021-01-16', 'DALTON KIPLETING', 'Male', 'Parent', '254701234567', 1416, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (79, '2024-09-24 06:32:52.008184', '2021-01-17', 'GERALD KIPKORIR', 'Male', 'Parent', '254701234567', 1417, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (80, '2024-09-24 06:32:52.016657', '2021-01-18', 'BRYLEE CHEPCHUMBA', 'Female', 'Parent', '254701234567', 1418, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (81, '2024-09-24 06:32:52.026191', '2021-01-19', 'JOY JERUTO', 'Female', 'Parent', '254701234567', 1419, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (82, '2024-09-24 06:32:52.033746', '2021-01-20', 'RYAN KIPSANG', 'Male', 'Parent', '254701234567', 1420, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (83, '2024-09-24 06:32:52.043215', '2021-01-21', 'LYEON KIMUTAI', 'Male', 'Parent', '254701234567', 1421, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (84, '2024-09-24 06:32:52.050457', '2021-01-22', 'ROY KIGEN', 'Male', 'Parent', '254701234567', 1422, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (85, '2024-09-24 06:32:52.058774', '2021-01-23', 'GODWILL KIPCHIRCHIR', 'Male', 'Parent', '254701234567', 1423, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (86, '2024-09-24 06:32:52.067239', '2021-01-24', 'JANISH JEMUTAI', 'Female', 'Parent', '254701234567', 1424, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (87, '2024-09-24 06:32:52.076442', '2021-01-25', 'SASHA JEMUTAI', 'Female', 'Parent', '254701234567', 1425, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (88, '2024-09-24 06:32:52.084763', '2021-01-26', 'PATIENCE JEBET', 'Female', 'Parent', '254701234567', 1426, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (89, '2024-09-24 06:32:52.093810', '2021-01-27', 'NICOLE JEPLETING', 'Female', 'Parent', '254701234567', 1427, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (90, '2024-09-24 06:32:52.101552', '2021-01-28', 'MERCY JEPKOECH', 'Female', 'Parent', '254701234567', 1428, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (91, '2024-09-24 06:32:52.111056', '2021-01-29', 'IAN KIPKOECH', 'Male', 'Parent', '254701234567', 1429, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (92, '2024-09-24 06:32:52.121032', '2021-01-30', 'JARED KIPROP', 'Male', 'Parent', '254701234567', 1430, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (93, '2024-09-24 06:32:52.131730', '2021-01-31', 'JAYDEN KIPNGETICH', 'Male', 'Parent', '254701234567', 1431, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (94, '2024-09-24 06:32:52.140723', '2021-02-01', 'MAYA JEPCHUMBA', 'Female', 'Parent', '254701234567', 1432, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (95, '2024-09-24 06:32:52.151474', '2021-02-02', 'PRECIOUS JEPCHIRCHIR', 'Female', 'Parent', '254701234567', 1433, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (96, '2024-09-24 06:32:52.161553', '2021-02-03', 'ALOYCIOUS KIPROP', 'Male', 'Parent', '254701234567', 1434, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (97, '2024-09-24 06:32:52.169208', '2021-02-04', 'RAY KIMURGOR', 'Male', 'Parent', '254701234567', 1435, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (98, '2024-09-24 06:32:52.177923', '2021-02-05', 'SHANE JEPTOO', 'Female', 'Parent', '254701234567', 1436, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (99, '2024-09-24 06:32:52.185705', '2021-02-06', 'RYAN KIBET', 'Male', 'Parent', '254701234567', 1437, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (100, '2024-09-24 06:32:52.195361', '2021-02-07', 'ANGEL CHEROP', 'Female', 'Parent', '254701234567', 1438, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (101, '2024-09-24 06:32:52.203407', '2021-02-08', 'STAVY JERUTO', 'Female', 'Parent', '254701234567', 1439, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (102, '2024-09-24 06:32:52.212180', '2021-02-09', 'GERALD KIMURGOR', 'Male', 'Parent', '254701234567', 1440, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (103, '2024-09-24 06:32:52.218435', '2021-02-10', 'LENZA CHELIMO', 'Female', 'Parent', '254701234567', 1441, 4, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (104, '2024-09-24 06:36:28.056446', '2021-01-01', 'SHAINA JOY JEBET', 'Female', 'Parent', '254701234567', 1501, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (105, '2024-09-24 06:36:28.065452', '2021-01-02', 'SHANTEL JEROP', 'Female', 'Parent', '254701234567', 1502, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (106, '2024-09-24 06:36:28.072448', '2021-01-03', 'SHANTEL JEROTICH', 'Female', 'Parent', '254701234567', 1503, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (107, '2024-09-24 06:36:28.081817', '2021-01-04', 'JULIET JEPTOO', 'Female', 'Parent', '254701234567', 1504, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (108, '2024-09-24 06:36:28.088571', '2021-01-05', 'SHERYL  JEROP', 'Female', 'Parent', '254701234567', 1505, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (109, '2024-09-24 06:36:28.101278', '2021-01-06', 'BLESSINGS JEMUTAI', 'Female', 'Parent', '254701234567', 1506, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (110, '2024-09-24 06:36:28.112204', '2021-01-07', 'TIFFANY JELIMO', 'Female', 'Parent', '254701234567', 1507, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (111, '2024-09-24 06:36:28.120214', '2021-01-08', 'SHAMIM JEPKOECH', 'Female', 'Parent', '254701234567', 1508, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (112, '2024-09-24 06:36:28.128202', '2021-01-09', 'SHANTEL JEPTOO', 'Female', 'Parent', '254701234567', 1509, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (113, '2024-09-24 06:36:28.136210', '2021-01-10', 'ELSY JERONO', 'Female', 'Parent', '254701234567', 1510, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (114, '2024-09-24 06:36:28.143207', '2021-01-11', 'ABIGAEL JEPTOO', 'Female', 'Parent', '254701234567', 1511, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (115, '2024-09-24 06:36:28.151204', '2021-01-12', 'SHERLY JEPTOO', 'Female', 'Parent', '254701234567', 1512, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (116, '2024-09-24 06:36:28.158204', '2021-01-13', 'VINN TREVOR KIPCHUMBA', 'Male', 'Parent', '254701234567', 1513, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (117, '2024-09-24 06:36:28.166210', '2021-01-14', 'SHANICE JEMURGOR', 'Female', 'Parent', '254701234567', 1514, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (118, '2024-09-24 06:36:28.172714', '2021-01-15', 'ARSHAVIN KIGEN', 'Male', 'Parent', '254701234567', 1515, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (119, '2024-09-24 06:36:28.179715', '2021-01-16', 'JAYDEN KIPCHIRCHIR', 'Male', 'Parent', '254701234567', 1516, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (120, '2024-09-24 06:36:28.186520', '2021-01-17', 'SHALEENJOY JERUTO', 'Female', 'Parent', '254701234567', 1517, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (121, '2024-09-24 06:36:28.192515', '2021-01-18', 'FELICE JEBET', 'Female', 'Parent', '254701234567', 1518, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (122, '2024-09-24 06:36:28.201723', '2021-01-19', 'ELSY JEPKORIR', 'Female', 'Parent', '254701234567', 1519, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (123, '2024-09-24 06:36:28.211731', '2021-01-20', 'JOY JEPCHUMBA', 'Female', 'Parent', '254701234567', 1520, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (124, '2024-09-24 06:36:28.221844', '2021-01-21', 'SHERYLE JEPCHUMBA', 'Female', 'Parent', '254701234567', 1521, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (125, '2024-09-24 06:36:28.234848', '2021-01-22', 'ELOCIOUS KIMURGOR', 'Male', 'Parent', '254701234567', 1522, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (126, '2024-09-24 06:36:28.250843', '2021-01-23', 'SHEM KIPRUTO', 'Male', 'Parent', '254701234567', 1523, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (127, '2024-09-24 06:36:28.261586', '2021-01-24', 'SHANTEL JEMUTAI', 'Female', 'Parent', '254701234567', 1524, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (128, '2024-09-24 06:36:28.274138', '2021-01-25', 'VICTOR KIPKOECH', 'Male', 'Parent', '254701234567', 1525, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (129, '2024-09-24 06:36:28.287331', '2021-01-26', 'NAZARENA JEPKORIR', 'Female', 'Parent', '254701234567', 1526, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (130, '2024-09-24 06:36:28.299335', '2021-01-27', 'SHANICE JERUTO', 'Female', 'Parent', '254701234567', 1527, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (131, '2024-09-24 06:36:28.310335', '2021-01-28', 'ERASTUS KIPRUTO', 'Male', 'Parent', '254701234567', 1528, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (132, '2024-09-24 06:36:28.322339', '2021-01-29', 'ERRICK KIMUTAI', 'Male', 'Parent', '254701234567', 1529, 5, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (133, '2024-09-24 06:41:52.135068', '2021-01-01', 'NEDDY JEPKOECH', 'Female', 'Parent', '254701234567', 1601, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (134, '2024-09-24 06:41:52.145421', '2021-01-02', 'GIFT JEPKOSKEI', 'Female', 'Parent', '254701234567', 1602, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (135, '2024-09-24 06:41:52.153301', '2021-01-03', 'DERRYN JEROTICH', 'Female', 'Parent', '254701234567', 1603, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (136, '2024-09-24 06:41:52.163092', '2021-01-04', 'MISHAEL KIPTOO', 'Male', 'Parent', '254701234567', 1604, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (137, '2024-09-24 06:41:52.171191', '2021-01-05', 'BRASON KIPCHUMBA', 'Male', 'Parent', '254701234567', 1605, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (138, '2024-09-24 06:41:52.181475', '2021-01-06', 'ADRIAN KIPKORIR', 'Male', 'Parent', '254701234567', 1606, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (139, '2024-09-24 06:41:52.188403', '2021-01-07', 'SHANTEL JERUTO', 'Female', 'Parent', '254701234567', 1607, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (140, '2024-09-24 06:41:52.196300', '2021-01-08', 'PAYDEN KIPRUTO', 'Male', 'Parent', '254701234567', 1608, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (141, '2024-09-24 06:41:52.203661', '2021-01-09', 'TREVOR KIMUTAI', 'Male', 'Parent', '254701234567', 1609, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (142, '2024-09-24 06:41:52.211280', '2021-01-10', 'FAITH CHEROP', 'Female', 'Parent', '254701234567', 1610, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (143, '2024-09-24 06:41:52.218038', '2021-01-11', 'IVY JEPCHUMBA', 'Female', 'Parent', '254701234567', 1611, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (144, '2024-09-24 06:41:52.226272', '2021-01-12', 'AORON KIGEN', 'Male', 'Parent', '254701234567', 1612, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (145, '2024-09-24 06:41:52.232252', '2021-01-13', 'SHANTEL JELIMO', 'Female', 'Parent', '254701234567', 1613, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (146, '2024-09-24 06:41:52.261518', '2021-01-14', 'BLESSINGS JELIMO', 'Female', 'Parent', '254701234567', 1614, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (147, '2024-09-24 06:41:52.313889', '2021-01-15', 'OLMPIA CHEPCHIRCHIR', 'Female', 'Parent', '254701234567', 1615, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (148, '2024-09-24 06:41:52.329424', '2021-01-16', 'MERCY JEPTOO', 'Female', 'Parent', '254701234567', 1616, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (149, '2024-09-24 06:41:52.344307', '2021-01-17', 'BRAVIN KIPCHUMBA', 'Male', 'Parent', '254701234567', 1617, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (150, '2024-09-24 06:41:52.368379', '2021-01-18', 'BLESSINGS JEPLETING', 'Female', 'Parent', '254701234567', 1618, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (151, '2024-09-24 06:41:52.382737', '2021-01-19', 'JAZEN KIMUTAI', 'Male', 'Parent', '254701234567', 1619, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (152, '2024-09-24 06:41:52.404055', '2021-01-20', 'BECKYFAITH JEMURGOR', 'Female', 'Parent', '254701234567', 1620, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (153, '2024-09-24 06:41:52.424453', '2021-01-21', 'SHIREEN JEPKIRUI', 'Female', 'Parent', '254701234567', 1621, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (154, '2024-09-24 06:41:52.443030', '2021-01-22', 'JOY JEBET', 'Female', 'Parent', '254701234567', 1622, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (155, '2024-09-24 06:41:52.463193', '2021-01-23', 'JOY BUSIENEI CHEMINING', 'Female', 'Parent', '254701234567', 1623, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (156, '2024-09-24 06:41:52.484316', '2021-01-24', 'LYNN JERONO', 'Female', 'Parent', '254701234567', 1624, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (157, '2024-09-24 06:41:52.502573', '2021-01-25', 'EMMANUEL KIPCHUMBA', 'Male', 'Parent', '254701234567', 1625, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (158, '2024-09-24 06:41:52.519897', '2021-01-26', 'OLIVER KIPCHUMBA', 'Male', 'Parent', '254701234567', 1626, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (159, '2024-09-24 06:41:52.535555', '2021-01-27', 'LAWRANCE KIPCHUMBA', 'Male', 'Parent', '254701234567', 1627, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (160, '2024-09-24 06:41:52.553594', '2021-01-28', 'JOY CHEMURGOR', 'Female', 'Parent', '254701234567', 1628, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (161, '2024-09-24 06:41:52.573049', '2021-01-29', 'SHERYL JEPKEMBOI', 'Female', 'Parent', '254701234567', 1629, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (162, '2024-09-24 06:41:52.587851', '2021-01-30', 'EZRON KIPCHUMBA', 'Male', 'Parent', '254701234567', 1630, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (163, '2024-09-24 06:41:52.608885', '2021-01-31', 'WAYNE KIPROP', 'Male', 'Parent', '254701234567', 1631, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (164, '2024-09-24 06:41:52.626159', '2021-02-01', 'SHABELLA JEPKEMBOI', 'Female', 'Parent', '254701234567', 1632, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (165, '2024-09-24 06:41:52.644521', '2021-02-02', 'FLAVIAN JEPKIRUI', 'Female', 'Parent', '254701234567', 1633, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (166, '2024-09-24 06:41:52.667215', '2021-02-03', 'ABIGGEL JEPCHUMBA', 'Female', 'Parent', '254701234567', 1634, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (167, '2024-09-24 06:41:52.682657', '2021-02-04', 'BYLON KIPRUTO ', 'Male', 'Parent', '254701234567', 1635, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (168, '2024-09-24 06:41:52.703500', '2021-02-05', 'MAXWEL KIPTOO', 'Male', 'Parent', '254701234567', 1636, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (169, '2024-09-24 06:41:52.723758', '2021-02-06', 'DAVIN KIPLAGAT', 'Male', 'Parent', '254701234567', 1637, 6, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (170, '2024-09-24 06:47:05.553084', '2021-01-01', 'IAN KIPLETING', 'Male', 'Parent', '254701234567', 1701, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (171, '2024-09-24 06:47:05.575743', '2021-01-02', 'SHARLINE  JERUTO', 'Female', 'Parent', '254701234567', 1702, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (172, '2024-09-24 06:47:05.599621', '2021-01-03', 'JOY JELAGAT', 'Female', 'Parent', '254701234567', 1703, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (173, '2024-09-24 06:47:05.620986', '2021-01-04', 'EMMANUEL KIMUTAI', 'Male', 'Parent', '254701234567', 1704, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (174, '2024-09-24 06:47:05.646921', '2021-01-05', 'BRAVIN KIPTOO', 'Male', 'Parent', '254701234567', 1705, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (175, '2024-09-24 06:47:05.673084', '2021-01-06', 'SHANTEL JEMURGOR', 'Female', 'Parent', '254701234567', 1706, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (176, '2024-09-24 06:47:05.696908', '2021-01-07', 'JOY JEPTOO', 'Female', 'Parent', '254701234567', 1707, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (177, '2024-09-24 06:47:05.719133', '2021-01-08', 'CALISTUS KIPCHUMBA', 'Male', 'Parent', '254701234567', 1708, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (178, '2024-09-24 06:47:05.728970', '2021-01-09', 'ABEL KIBOR', 'Male', 'Parent', '254701234567', 1709, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (179, '2024-09-24 06:47:05.739674', '2021-01-10', 'JOHN KIPTANUI', 'Male', 'Parent', '254701234567', 1710, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (180, '2024-09-24 06:47:05.747040', '2021-01-11', 'RENCY JERUTO', 'Female', 'Parent', '254701234567', 1711, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (181, '2024-09-24 06:47:05.754500', '2021-01-12', 'GODIUS KIPRUTO', 'Male', 'Parent', '254701234567', 1712, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (182, '2024-09-24 06:47:05.761504', '2021-01-13', 'FAITH JERUTO', 'Female', 'Parent', '254701234567', 1713, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (183, '2024-09-24 06:47:05.769262', '2021-01-14', 'JAYDEN KIPRUTO', 'Male', 'Parent', '254701234567', 1714, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (184, '2024-09-24 06:47:05.775607', '2021-01-15', 'CALISTUS KIMUTAI', 'Male', 'Parent', '254701234567', 1715, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (185, '2024-09-24 06:47:05.782189', '2021-01-16', 'BRAMWEL KIPKEMBOI', 'Male', 'Parent', '254701234567', 1716, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (186, '2024-09-24 06:47:05.789506', '2021-01-17', 'AIDEN KIPCHIRCHIR', 'Male', 'Parent', '254701234567', 1717, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (187, '2024-09-24 06:47:05.797107', '2021-01-18', 'AMBROSE KIPKEMBOI', 'Male', 'Parent', '254701234567', 1718, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (188, '2024-09-24 06:47:05.807964', '2021-01-19', 'SHADRACK KIMUTAI', 'Male', 'Parent', '254701234567', 1719, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (189, '2024-09-24 06:47:05.815289', '2021-01-20', 'ALVINE KIPKOSGEI', 'Male', 'Parent', '254701234567', 1720, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (190, '2024-09-24 06:47:05.823771', '2021-01-21', 'JABEZ KIPCHUMBA', 'Male', 'Parent', '254701234567', 1721, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (191, '2024-09-24 06:47:05.830160', '2021-01-22', 'PRECIOUS JEROP', 'Female', 'Parent', '254701234567', 1722, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (192, '2024-09-24 06:47:05.837188', '2021-01-23', 'BRIAN KIMUTAI', 'Male', 'Parent', '254701234567', 1723, 7, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (193, '2024-09-24 06:50:05.948846', '2021-01-01', 'SHERYL JEPTOO', 'Female', 'Parent', '254701234567', 1801, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (194, '2024-09-24 06:50:05.959005', '2021-01-02', 'SHANICE JEPCHUMBA', 'Female', 'Parent', '254701234567', 1802, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (195, '2024-09-24 06:50:05.969347', '2021-01-03', 'CLARE JEPCHIRCHIR', 'Female', 'Parent', '254701234567', 1803, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (196, '2024-09-24 06:50:05.980062', '2021-01-04', 'SHANTEL JEPNGETICH', 'Female', 'Parent', '254701234567', 1804, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (197, '2024-09-24 06:50:05.988399', '2021-01-05', 'NOEL KIPLETING', 'Male', 'Parent', '254701234567', 1805, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (198, '2024-09-24 06:50:05.997106', '2021-01-06', 'ASBEL KIGEN', 'Male', 'Parent', '254701234567', 1806, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (199, '2024-09-24 06:50:06.003296', '2021-01-07', 'IVINE JEPCHUMBA', 'Female', 'Parent', '254701234567', 1807, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (200, '2024-09-24 06:50:06.012580', '2021-01-08', 'ABEL KIPRUTO', 'Male', 'Parent', '254701234567', 1808, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (201, '2024-09-24 06:50:06.019896', '2021-01-09', 'TIFFANY BLESSINGS JEBET', 'Female', 'Parent', '254701234567', 1809, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (202, '2024-09-24 06:50:06.027390', '2021-01-10', 'NICOLE JEPKOSGEI', 'Female', 'Parent', '254701234567', 1810, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (203, '2024-09-24 06:50:06.034553', '2021-01-11', 'JABEZ KIPLIMO', 'Male', 'Parent', '254701234567', 1811, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (204, '2024-09-24 06:50:06.041467', '2021-01-12', 'JOY JEROP', 'Female', 'Parent', '254701234567', 1812, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (205, '2024-09-24 06:50:06.049583', '2021-01-13', 'ANASTASIA JEPKEMBOI', 'Female', 'Parent', '254701234567', 1813, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (206, '2024-09-24 06:50:06.057001', '2021-01-14', 'SHARLINE JEPCHUMBA', 'Female', 'Parent', '254701234567', 1814, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (207, '2024-09-24 06:50:06.064912', '2021-01-15', 'NICKSON KIPRUTO', 'Male', 'Parent', '254701234567', 1815, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (208, '2024-09-24 06:50:06.072781', '2021-01-16', 'BENEDIN JEPCHUMBA', 'Female', 'Parent', '254701234567', 1816, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (209, '2024-09-24 06:50:06.080744', '2021-01-17', 'BASIL KIPCHUMBA', 'Male', 'Parent', '254701234567', 1817, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (210, '2024-09-24 06:50:06.089277', '2021-01-18', 'NORMAN KIPCHUMBA', 'Male', 'Parent', '254701234567', 1818, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (211, '2024-09-24 06:50:06.096559', '2021-01-19', 'GYNECIOUS KIMURGOR', 'Male', 'Parent', '254701234567', 1819, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (212, '2024-09-24 06:50:06.102716', '2021-01-20', 'JOY JEPKORIR', 'Female', 'Parent', '254701234567', 1820, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (213, '2024-09-24 06:50:06.110798', '2021-01-21', 'VALARY JEPCHUMBA', 'Female', 'Parent', '254701234567', 1821, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (214, '2024-09-24 06:50:06.118511', '2021-01-22', 'MERCY JELIMO', 'Female', 'Parent', '254701234567', 1822, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (215, '2024-09-24 06:50:06.126594', '2021-01-23', 'MYLES KIBET', 'Male', 'Parent', '254701234567', 1823, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (216, '2024-09-24 06:50:06.133918', '2021-01-24', 'WAYNE KIPROTICH', 'Male', 'Parent', '254701234567', 1824, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (217, '2024-09-24 06:50:06.140535', '2021-01-25', 'MELVIN JELAGAT', 'Female', 'Parent', '254701234567', 1825, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (218, '2024-09-24 06:50:06.149776', '2021-01-26', 'BRIGHTON KIPCHUMBA', 'Male', 'Parent', '254701234567', 1826, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (219, '2024-09-24 06:50:06.157094', '2021-01-27', 'ABEL KIMUTAI', 'Male', 'Parent', '254701234567', 1827, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (220, '2024-09-24 06:50:06.164692', '2021-01-28', 'RYAN KIPRUTO', 'Male', 'Parent', '254701234567', 1828, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (221, '2024-09-24 06:50:06.172120', '2021-01-29', 'SHELVIN JEPCHUMBA', 'Female', 'Parent', '254701234567', 1829, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (222, '2024-09-24 06:50:06.180800', '2021-01-30', 'JOSHUA ODUPOI', 'Male', 'Parent', '254701234567', 1830, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (223, '2024-09-24 06:50:06.187968', '2021-01-31', 'ALEX KIPKOSGEI', 'Male', 'Parent', '254701234567', 1831, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (224, '2024-09-24 06:50:06.194830', '2021-01-01', 'ASBEL KIPLAGAT', 'Male', 'Parent', '254701234567', 1832, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (225, '2024-09-24 06:50:06.202109', '2021-01-02', 'MERCY JEPTOO', 'Female', 'Parent', '254701234567', 1833, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (226, '2024-09-24 06:50:06.209567', '2021-01-03', 'JAYDEN KIBET', 'Male', 'Parent', '254701234567', 1834, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (227, '2024-09-24 06:50:06.216543', '2021-01-04', 'LYNE JEPCHUMBA', 'Female', 'Parent', '254701234567', 1835, 8, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (228, '2024-09-24 06:57:43.418470', '2021-01-01', 'FABIAN KIPCHIRCHIR', 'Male', 'Parent', '254701234567', 1901, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (229, '2024-09-24 06:57:43.434518', '2021-01-02', 'LELIA JEMUTAI', 'Female', 'Parent', '254701234567', 1902, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (230, '2024-09-24 06:57:43.448080', '2021-01-03', 'JESSY KIMUTAI', 'Female', 'Parent', '254701234567', 1903, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (231, '2024-09-24 06:57:43.465606', '2021-01-04', 'SAMWEL MBUGUA', 'Female', 'Parent', '254701234567', 1904, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (232, '2024-09-24 06:57:43.483617', '2021-01-05', 'MERCY CHEMUTAI', 'Male', 'Parent', '254701234567', 1905, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (233, '2024-09-24 06:57:43.501873', '2021-01-06', 'RYAN NGISIREY', 'Male', 'Parent', '254701234567', 1906, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (234, '2024-09-24 06:57:43.521965', '2021-01-07', 'AUDREY CHEROP', 'Female', 'Parent', '254701234567', 1907, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (235, '2024-09-24 06:57:43.548430', '2021-01-08', 'BLESSING KIPCHUMBA', 'Male', 'Parent', '254701234567', 1908, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (236, '2024-09-24 06:57:43.564896', '2021-01-09', 'AURELIA JEPKOGEI', 'Female', 'Parent', '254701234567', 1909, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (237, '2024-09-24 06:57:43.584295', '2021-01-10', 'BRAVIN KIPKIRUI', 'Female', 'Parent', '254701234567', 1910, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (238, '2024-09-24 06:57:43.601977', '2021-01-11', 'PHILIS JEPKOECH', 'Male', 'Parent', '254701234567', 1911, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (239, '2024-09-24 06:57:43.612239', '2021-01-12', 'MITCHELLE JERONO', 'Female', 'Parent', '254701234567', 1912, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (240, '2024-09-24 06:57:43.620598', '2021-01-13', ' ALLAN KIPKOSGEI', 'Female', 'Parent', '254701234567', 1913, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (241, '2024-09-24 06:57:43.633514', '2021-01-14', 'FAITH JEPKORIR', 'Female', 'Parent', '254701234567', 1914, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (242, '2024-09-24 06:57:43.644296', '2021-01-15', 'IAN KIBET', 'Male', 'Parent', '254701234567', 1915, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (243, '2024-09-24 06:57:43.653945', '2021-01-16', 'ANNICETUS JELAGAT', 'Female', 'Parent', '254701234567', 1916, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (244, '2024-09-24 06:57:43.665134', '2021-01-17', 'JOY CHEPTOO', 'Male', 'Parent', '254701234567', 1917, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (245, '2024-09-24 06:57:43.674417', '2021-01-18', 'EMMAN KIPRUTO', 'Male', 'Parent', '254701234567', 1918, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (246, '2024-09-24 06:57:43.683041', '2021-01-19', 'JAVAN KIMURGOR', 'Male', 'Parent', '254701234567', 1919, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (247, '2024-09-24 06:57:43.693947', '2021-01-20', 'BRIAN KIPCHUMBA', 'Female', 'Parent', '254701234567', 1920, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (248, '2024-09-24 06:57:43.701694', '2021-01-21', 'MERCY CHEPCHUMBA', 'Female', 'Parent', '254701234567', 1921, 9, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (249, '2024-09-24 07:01:22.211546', '2021-01-01', 'MESHACK KIPROTICH', 'Male', 'Parent', '254701234567', 2401, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (250, '2024-09-24 07:01:22.223851', '2021-01-02', 'NATANIA CHEPKOECH', 'Female', 'Parent', '254701234567', 2402, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (251, '2024-09-24 07:01:22.231048', '2021-01-03', 'JOY JELIMO', 'Female', 'Parent', '254701234567', 2403, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (252, '2024-09-24 07:01:22.236448', '2021-01-04', 'SHIRLINE JEPKOECH', 'Female', 'Parent', '254701234567', 2404, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (253, '2024-09-24 07:01:22.244358', '2021-01-05', 'ABIGAEL JERONO', 'Female', 'Parent', '254701234567', 2405, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (254, '2024-09-24 07:01:22.251252', '2021-01-06', 'JOY CHEPKOSGEI', 'Female', 'Parent', '254701234567', 2406, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (255, '2024-09-24 07:01:22.257951', '2021-01-07', 'SHEM KIPLIMO', 'Male', 'Parent', '254701234567', 2407, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (256, '2024-09-24 07:01:22.265210', '2021-01-08', 'MARK KIPKOECH', 'Male', 'Parent', '254701234567', 2408, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (257, '2024-09-24 07:01:22.271909', '2021-01-09', 'ADELINE JEBICHII', 'Female', 'Parent', '254701234567', 2409, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (258, '2024-09-24 07:01:22.278635', '2021-01-10', 'FAITH JEROTICH', 'Female', 'Parent', '254701234567', 2410, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (259, '2024-09-24 07:01:22.285827', '2021-01-11', 'EMMANUEL K SOIMO', 'Male', 'Parent', '254701234567', 2411, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (260, '2024-09-24 07:01:22.292475', '2021-01-12', 'EMMANUEL KIPRONO', 'Male', 'Parent', '254701234567', 2412, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (261, '2024-09-24 07:01:22.299973', '2021-01-13', 'NICHOLAS CHERUIYOT', 'Male', 'Parent', '254701234567', 2413, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (262, '2024-09-24 07:01:22.307403', '2021-01-14', 'SHERLYN JEMUTAI ', 'Female', 'Parent', '254701234567', 2414, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (263, '2024-09-24 07:01:22.314970', '2021-01-15', 'ALLAN KIPLAGAT', 'Male', 'Parent', '254701234567', 2415, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (264, '2024-09-24 07:01:22.322263', '2021-01-16', 'DISMAS KIPKURUI', 'Male', 'Parent', '254701234567', 2416, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (265, '2024-09-24 07:01:22.328694', '2021-01-17', 'SASHA JEROTICH', 'Female', 'Parent', '254701234567', 2417, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (266, '2024-09-24 07:01:22.334200', '2021-01-18', 'ANTHONIUS CHERUIYOT', 'Male', 'Parent', '254701234567', 2418, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (267, '2024-09-24 07:01:22.341783', '2021-01-19', 'JOY JELAGAT', 'Female', 'Parent', '254701234567', 2419, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (268, '2024-09-24 07:01:22.349176', '2021-01-20', 'EMMANUEL KIBET', 'Male', 'Parent', '254701234567', 2420, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (269, '2024-09-24 07:01:22.356591', '2021-01-21', 'MARVELYNE JEMUTAI', 'Female', 'Parent', '254701234567', 2421, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (270, '2024-09-24 07:01:22.363468', '2021-01-22', 'GRIFFIN KIRWA', 'Male', 'Parent', '254701234568', 2422, 10, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (271, '2024-09-24 07:03:20.761903', '2021-01-01', 'JUDE ELI KIPRUTO', 'Male', 'Parent', '254701234567', 2301, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (272, '2024-09-24 07:03:20.773396', '2021-01-02', 'BRANDON CHERUIYOT', 'Male', 'Parent', '254701234567', 2302, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (273, '2024-09-24 07:03:20.782396', '2021-01-03', 'MERCY JEPKOECH', 'Female', 'Parent', '254701234567', 2303, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (274, '2024-09-24 07:03:20.791955', '2021-01-04', 'BRIAN KIPROTICH', 'Male', 'Parent', '254701234567', 2304, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (275, '2024-09-24 07:03:20.801054', '2021-01-05', 'ABIGAEL JELAGAT', 'Female', 'Parent', '254701234567', 2305, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (276, '2024-09-24 07:03:20.811242', '2021-01-06', 'BLESSING NJERI', 'Female', 'Parent', '254701234567', 2306, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (277, '2024-09-24 07:03:20.821033', '2021-01-07', 'BRIMIN KIPCHUMBA', 'Male', 'Parent', '254701234567', 2307, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (278, '2024-09-24 07:03:20.829785', '2021-01-08', 'OLIVIA JEBET', 'Female', 'Parent', '254701234567', 2308, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (279, '2024-09-24 07:03:20.841121', '2021-01-09', 'SHERILEEN SASHA', 'Female', 'Parent', '254701234567', 2309, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (280, '2024-09-24 07:03:20.848767', '2021-01-10', 'MARGARET NJERI', 'Female', 'Parent', '254701234567', 2310, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (281, '2024-09-24 07:03:20.859300', '2021-01-11', 'LIZCOLE JEPKIRUI RUTO', 'Female', 'Parent', '254701234567', 2311, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (282, '2024-09-24 07:03:20.866615', '2021-01-12', 'SHERRYL JEPCHUMBA', 'Female', 'Parent', '254701234567', 2312, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (283, '2024-09-24 07:03:20.877126', '2021-01-13', 'CAROLINE CHEPCHUMBA', 'Female', 'Parent', '254701234567', 2313, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (284, '2024-09-24 07:03:20.885394', '2021-01-14', 'CORNELIUS KIMURGOR', 'Male', 'Parent', '254701234567', 2314, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (285, '2024-09-24 07:03:20.895851', '2021-01-15', 'JOAN JEPKORIR', 'Female', 'Parent', '254701234567', 2315, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (286, '2024-09-24 07:03:20.904536', '2021-01-16', 'PATIENCE CHEPKEMEI', 'Female', 'Parent', '254701234567', 2316, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (287, '2024-09-24 07:03:20.915575', '2021-01-17', 'MITCHEL JEPCHUMBA', 'Female', 'Parent', '254701234567', 2317, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (288, '2024-09-24 07:03:20.927639', '2021-01-18', 'WAYNE KIPKOECH', 'Male', 'Parent', '254701234567', 2318, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (289, '2024-09-24 07:03:20.939591', '2021-01-19', 'MEDRINE JELAGAT', 'Female', 'Parent', '254701234567', 2319, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (290, '2024-09-24 07:03:20.949539', '2021-01-20', 'CYNTHIA JEMUTAI', 'Female', 'Parent', '254701234567', 2320, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (291, '2024-09-24 07:03:20.961437', '2021-01-21', 'VINCENT KIPKEMBOI', 'Male', 'Parent', '254701234567', 2321, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (292, '2024-09-24 07:03:20.969987', '2021-01-22', 'MARVINE KIPKEMBOI', 'Male', 'Parent', '254701234568', 2322, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (293, '2024-09-24 07:03:20.981361', '2021-01-23', 'PRECIOUS JEPTOO', 'Female', 'Parent', '254701234569', 2323, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (294, '2024-09-24 07:03:20.992414', '2021-01-24', 'MITCHEL  JELIMO', 'Female', 'Parent', '254701234570', 2324, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (295, '2024-09-24 07:03:21.001398', '2021-01-25', 'KEVIN KIPRUTO', 'Male', 'Parent', '254701234571', 2325, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (296, '2024-09-24 07:03:21.013121', '2021-01-26', 'LUCKY KIPCHUMBA', 'Male', 'Parent', '254701234572', 2326, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (297, '2024-09-24 07:03:21.023648', '2021-01-27', 'BRIAN KIPYEGO', 'Male', 'Parent', '254701234573', 2327, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (298, '2024-09-24 07:03:21.032643', '2021-01-28', 'KELVINE KIPCHIRCHIR', 'Male', 'Parent', '254701234574', 2328, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (299, '2024-09-24 07:03:21.044428', '2021-01-29', 'ELLY KIPTOO', 'Male', 'Parent', '254701234575', 2329, 11, 0, 0, 0);
INSERT INTO learners_learnerregister (id, register_date, date_of_birth, name, gender, name_of_parent, parent_contact, learner_id, grade_id, beans_balance, fee_balance, maize_balance) VALUES (300, '2024-09-24 07:03:21.055973', '2021-01-30', 'YUSUF KIPCHUMBA', 'Male', 'Parent', '254701234576', 2330, 11, 0, 0, 0);

-- Table: learners_school
CREATE TABLE IF NOT EXISTS "learners_school" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "principal_remark" text NOT NULL);

-- Index: administrator_attendance_learner_id_0c01542d
CREATE INDEX IF NOT EXISTS "administrator_attendance_learner_id_0c01542d" ON "administrator_attendance" ("learner_id");

-- Index: administrator_attendance_learner_id_date_7826bde7_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "administrator_attendance_learner_id_date_7826bde7_uniq" ON "administrator_attendance" ("learner_id", "date");

-- Index: administrator_curriculum_grade_id_5dab9d6a
CREATE INDEX IF NOT EXISTS "administrator_curriculum_grade_id_5dab9d6a" ON "administrator_curriculum" ("grade_id");

-- Index: administrator_curriculum_subjects_curriculum_id_8b3ff9c7
CREATE INDEX IF NOT EXISTS "administrator_curriculum_subjects_curriculum_id_8b3ff9c7" ON "administrator_curriculum_subjects" ("curriculum_id");

-- Index: administrator_curriculum_subjects_curriculum_id_subject_id_8ee6ffdc_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "administrator_curriculum_subjects_curriculum_id_subject_id_8ee6ffdc_uniq" ON "administrator_curriculum_subjects" ("curriculum_id", "subject_id");

-- Index: administrator_curriculum_subjects_subject_id_d53b9c74
CREATE INDEX IF NOT EXISTS "administrator_curriculum_subjects_subject_id_d53b9c74" ON "administrator_curriculum_subjects" ("subject_id");

-- Index: administrator_teacher_subjects_subject_id_522572e7
CREATE INDEX IF NOT EXISTS "administrator_teacher_subjects_subject_id_522572e7" ON "administrator_teacher_subjects" ("subject_id");

-- Index: administrator_teacher_subjects_teacher_id_d4f25b05
CREATE INDEX IF NOT EXISTS "administrator_teacher_subjects_teacher_id_d4f25b05" ON "administrator_teacher_subjects" ("teacher_id");

-- Index: administrator_teacher_subjects_teacher_id_subject_id_ea8ae213_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "administrator_teacher_subjects_teacher_id_subject_id_ea8ae213_uniq" ON "administrator_teacher_subjects" ("teacher_id", "subject_id");

-- Index: administrator_teacherassignment_grade_id_f1114763
CREATE INDEX IF NOT EXISTS "administrator_teacherassignment_grade_id_f1114763" ON "administrator_teacherassignment" ("grade_id");

-- Index: administrator_teacherassignment_subject_id_0f4b8e06
CREATE INDEX IF NOT EXISTS "administrator_teacherassignment_subject_id_0f4b8e06" ON "administrator_teacherassignment" ("subject_id");

-- Index: administrator_teacherassignment_teacher_id_e98894e4
CREATE INDEX IF NOT EXISTS "administrator_teacherassignment_teacher_id_e98894e4" ON "administrator_teacherassignment" ("teacher_id");

-- Index: administrator_teacherassignment_teacher_id_grade_id_subject_id_d341939c_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "administrator_teacherassignment_teacher_id_grade_id_subject_id_d341939c_uniq" ON "administrator_teacherassignment" ("teacher_id", "grade_id", "subject_id");

-- Index: administrator_timetable_grade_id_bd125b59
CREATE INDEX IF NOT EXISTS "administrator_timetable_grade_id_bd125b59" ON "administrator_timetable" ("grade_id");

-- Index: administrator_timetable_grade_id_day_start_time_6a1addb7_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "administrator_timetable_grade_id_day_start_time_6a1addb7_uniq" ON "administrator_timetable" ("grade_id", "day", "start_time");

-- Index: administrator_timetable_subject_id_c1387899
CREATE INDEX IF NOT EXISTS "administrator_timetable_subject_id_c1387899" ON "administrator_timetable" ("subject_id");

-- Index: auth_group_permissions_group_id_b120cbf9
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");

-- Index: auth_group_permissions_group_id_permission_id_0cd325b0_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");

-- Index: auth_group_permissions_permission_id_84c5c92e
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");

-- Index: auth_permission_content_type_id_2f476e4b
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");

-- Index: auth_permission_content_type_id_codename_01ab375a_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");

-- Index: auth_user_groups_group_id_97559544
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" ("group_id");

-- Index: auth_user_groups_user_id_6a12ed8b
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" ("user_id");

-- Index: auth_user_groups_user_id_group_id_94350c0c_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" ("user_id", "group_id");

-- Index: auth_user_user_permissions_permission_id_1fbb5f2c
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" ("permission_id");

-- Index: auth_user_user_permissions_user_id_a95ead1b
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" ("user_id");

-- Index: auth_user_user_permissions_user_id_permission_id_14a6b632_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" ("user_id", "permission_id");

-- Index: authenticator_custompermission_content_type_id_ac31f8c5
CREATE INDEX IF NOT EXISTS authenticator_custompermission_content_type_id_ac31f8c5 ON authenticator_custompermission ("content_type_id");

-- Index: authenticator_customuser_custom_permissions_custompermission_id_c0e6a613
CREATE INDEX IF NOT EXISTS authenticator_customuser_custom_permissions_custompermission_id_c0e6a613 ON authenticator_customuser_custom_permissions ("custompermission_id");

-- Index: authenticator_customuser_custom_permissions_customuser_id_b28f4e74
CREATE INDEX IF NOT EXISTS authenticator_customuser_custom_permissions_customuser_id_b28f4e74 ON authenticator_customuser_custom_permissions ("customuser_id");

-- Index: authenticator_customuser_custom_permissions_customuser_id_custompermission_id_56d2adba_uniq
CREATE UNIQUE INDEX IF NOT EXISTS authenticator_customuser_custom_permissions_customuser_id_custompermission_id_56d2adba_uniq ON authenticator_customuser_custom_permissions ("customuser_id", "custompermission_id");

-- Index: authenticator_customuser_groups_customuser_id_d83a5137
CREATE INDEX IF NOT EXISTS authenticator_customuser_groups_customuser_id_d83a5137 ON authenticator_customuser_groups ("customuser_id");

-- Index: authenticator_customuser_groups_customuser_id_group_id_c9870922_uniq
CREATE UNIQUE INDEX IF NOT EXISTS authenticator_customuser_groups_customuser_id_group_id_c9870922_uniq ON authenticator_customuser_groups ("customuser_id", "group_id");

-- Index: authenticator_customuser_groups_group_id_5e3020a1
CREATE INDEX IF NOT EXISTS authenticator_customuser_groups_group_id_5e3020a1 ON authenticator_customuser_groups ("group_id");

-- Index: authenticator_customuser_role_id_02e53484
CREATE INDEX IF NOT EXISTS authenticator_customuser_role_id_02e53484 ON authenticator_customuser ("role_id");

-- Index: authenticator_customuser_user_permissions_customuser_id_0afed486
CREATE INDEX IF NOT EXISTS authenticator_customuser_user_permissions_customuser_id_0afed486 ON authenticator_customuser_user_permissions ("customuser_id");

-- Index: authenticator_customuser_user_permissions_customuser_id_permission_id_3827e8e8_uniq
CREATE UNIQUE INDEX IF NOT EXISTS authenticator_customuser_user_permissions_customuser_id_permission_id_3827e8e8_uniq ON authenticator_customuser_user_permissions ("customuser_id", "permission_id");

-- Index: authenticator_customuser_user_permissions_permission_id_134e1583
CREATE INDEX IF NOT EXISTS authenticator_customuser_user_permissions_permission_id_134e1583 ON authenticator_customuser_user_permissions ("permission_id");

-- Index: authenticator_rolepermission_permission_id_f008ea6d
CREATE INDEX IF NOT EXISTS authenticator_rolepermission_permission_id_f008ea6d ON authenticator_rolepermission ("permission_id");

-- Index: authenticator_rolepermission_role_id_59c71c84
CREATE INDEX IF NOT EXISTS authenticator_rolepermission_role_id_59c71c84 ON authenticator_rolepermission ("role_id");

-- Index: authenticator_rolepermission_role_id_permission_id_afdc9e4f_uniq
CREATE UNIQUE INDEX IF NOT EXISTS authenticator_rolepermission_role_id_permission_id_afdc9e4f_uniq ON authenticator_rolepermission ("role_id", "permission_id");

-- Index: django_admin_log_content_type_id_c4bce8eb
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");

-- Index: django_admin_log_user_id_c564eba6
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");

-- Index: django_content_type_app_label_model_76bd3d3b_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");

-- Index: django_session_expire_date_a5c62663
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");

-- Index: exams_attendance_learner_id_date_02b6231d_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "exams_attendance_learner_id_date_02b6231d_uniq" ON "exams_attendance" ("learner_id", "date");

-- Index: exams_attendance_learner_id_dcedd082
CREATE INDEX IF NOT EXISTS "exams_attendance_learner_id_dcedd082" ON "exams_attendance" ("learner_id");

-- Index: exams_behavioralassessment_exam_type_id_f3e6057c
CREATE INDEX IF NOT EXISTS "exams_behavioralassessment_exam_type_id_f3e6057c" ON "exams_behavioralassessment" ("exam_type_id");

-- Index: exams_behavioralassessment_learner_id_fffe677c
CREATE INDEX IF NOT EXISTS "exams_behavioralassessment_learner_id_fffe677c" ON "exams_behavioralassessment" ("learner_id");

-- Index: exams_examresult_exam_type_id_10abe36f
CREATE INDEX IF NOT EXISTS "exams_examresult_exam_type_id_10abe36f" ON "exams_examresult" ("exam_type_id");

-- Index: exams_examresult_learner_id_id_b78fe3aa
CREATE INDEX IF NOT EXISTS "exams_examresult_learner_id_id_b78fe3aa" ON "exams_examresult" ("learner_id_id");

-- Index: exams_examresult_learner_id_id_subject_id_exam_type_id_e4e38377_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "exams_examresult_learner_id_id_subject_id_exam_type_id_e4e38377_uniq" ON "exams_examresult" ("learner_id_id", "subject_id", "exam_type_id");

-- Index: exams_examresult_subject_id_90675021
CREATE INDEX IF NOT EXISTS "exams_examresult_subject_id_90675021" ON "exams_examresult" ("subject_id");

-- Index: exams_extracurricularactivity_exam_type_id_bb5435ae
CREATE INDEX IF NOT EXISTS "exams_extracurricularactivity_exam_type_id_bb5435ae" ON "exams_extracurricularactivity" ("exam_type_id");

-- Index: exams_extracurricularactivity_learner_id_4fa6e63b
CREATE INDEX IF NOT EXISTS "exams_extracurricularactivity_learner_id_4fa6e63b" ON "exams_extracurricularactivity" ("learner_id");

-- Index: exams_learnertotalscore_exam_type_id_2a59079a
CREATE INDEX IF NOT EXISTS "exams_learnertotalscore_exam_type_id_2a59079a" ON "exams_learnertotalscore" ("exam_type_id");

-- Index: exams_learninggoal_exam_type_id_dfa92aac
CREATE INDEX IF NOT EXISTS "exams_learninggoal_exam_type_id_dfa92aac" ON "exams_learninggoal" ("exam_type_id");

-- Index: exams_learninggoal_learner_id_3741e92e
CREATE INDEX IF NOT EXISTS "exams_learninggoal_learner_id_3741e92e" ON "exams_learninggoal" ("learner_id");

-- Index: exams_progressreport_exam_type_id_ec7ab067
CREATE INDEX IF NOT EXISTS "exams_progressreport_exam_type_id_ec7ab067" ON "exams_progressreport" ("exam_type_id");

-- Index: exams_progressreport_learner_id_8208c2a8
CREATE INDEX IF NOT EXISTS "exams_progressreport_learner_id_8208c2a8" ON "exams_progressreport" ("learner_id");

-- Index: exams_progressreport_learner_id_exam_type_id_faceb9e2_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "exams_progressreport_learner_id_exam_type_id_faceb9e2_uniq" ON "exams_progressreport" ("learner_id", "exam_type_id");

-- Index: exams_skillsassessment_exam_type_id_aad86d51
CREATE INDEX IF NOT EXISTS "exams_skillsassessment_exam_type_id_aad86d51" ON "exams_skillsassessment" ("exam_type_id");

-- Index: exams_skillsassessment_learner_id_4bfae2fa
CREATE INDEX IF NOT EXISTS "exams_skillsassessment_learner_id_4bfae2fa" ON "exams_skillsassessment" ("learner_id");

-- Index: exams_socialemotionaldevelopment_exam_type_id_d4740b16
CREATE INDEX IF NOT EXISTS "exams_socialemotionaldevelopment_exam_type_id_d4740b16" ON "exams_socialemotionaldevelopment" ("exam_type_id");

-- Index: exams_socialemotionaldevelopment_learner_id_3dff3afd
CREATE INDEX IF NOT EXISTS "exams_socialemotionaldevelopment_learner_id_3dff3afd" ON "exams_socialemotionaldevelopment" ("learner_id");

-- Index: exams_specialachievement_exam_type_id_30a9580f
CREATE INDEX IF NOT EXISTS "exams_specialachievement_exam_type_id_30a9580f" ON "exams_specialachievement" ("exam_type_id");

-- Index: exams_specialachievement_learner_id_e06ddb09
CREATE INDEX IF NOT EXISTS "exams_specialachievement_learner_id_e06ddb09" ON "exams_specialachievement" ("learner_id");

-- Index: exams_standardizedtestscore_exam_type_id_f3ffe3af
CREATE INDEX IF NOT EXISTS "exams_standardizedtestscore_exam_type_id_f3ffe3af" ON "exams_standardizedtestscore" ("exam_type_id");

-- Index: exams_standardizedtestscore_learner_id_6bbed2aa
CREATE INDEX IF NOT EXISTS "exams_standardizedtestscore_learner_id_6bbed2aa" ON "exams_standardizedtestscore" ("learner_id");

-- Index: exams_studyhabit_exam_type_id_5b8ed1c2
CREATE INDEX IF NOT EXISTS "exams_studyhabit_exam_type_id_5b8ed1c2" ON "exams_studyhabit" ("exam_type_id");

-- Index: exams_studyhabit_learner_id_7a61b6a4
CREATE INDEX IF NOT EXISTS "exams_studyhabit_learner_id_7a61b6a4" ON "exams_studyhabit" ("learner_id");

-- Index: exams_subject_grades_grade_id_3427d3ff
CREATE INDEX IF NOT EXISTS "exams_subject_grades_grade_id_3427d3ff" ON "exams_subject_grades" ("grade_id");

-- Index: exams_subject_grades_subject_id_44262c74
CREATE INDEX IF NOT EXISTS "exams_subject_grades_subject_id_44262c74" ON "exams_subject_grades" ("subject_id");

-- Index: exams_subject_grades_subject_id_grade_id_ed7a8e7a_uniq
CREATE UNIQUE INDEX IF NOT EXISTS "exams_subject_grades_subject_id_grade_id_ed7a8e7a_uniq" ON "exams_subject_grades" ("subject_id", "grade_id");

-- Index: exams_supportservice_exam_type_id_4af538a7
CREATE INDEX IF NOT EXISTS "exams_supportservice_exam_type_id_4af538a7" ON "exams_supportservice" ("exam_type_id");

-- Index: exams_supportservice_learner_id_75105342
CREATE INDEX IF NOT EXISTS "exams_supportservice_learner_id_75105342" ON "exams_supportservice" ("learner_id");

-- Index: exams_teachercomment_exam_type_id_57d2f052
CREATE INDEX IF NOT EXISTS "exams_teachercomment_exam_type_id_57d2f052" ON "exams_teachercomment" ("exam_type_id");

-- Index: exams_teachercomment_learner_id_f0230ac6
CREATE INDEX IF NOT EXISTS "exams_teachercomment_learner_id_f0230ac6" ON "exams_teachercomment" ("learner_id");

-- Index: exams_teachercomment_subject_id_d8791f80
CREATE INDEX IF NOT EXISTS "exams_teachercomment_subject_id_d8791f80" ON "exams_teachercomment" ("subject_id");

-- Index: exams_teachercomment_teacher_id_0a624a43
CREATE INDEX IF NOT EXISTS "exams_teachercomment_teacher_id_0a624a43" ON "exams_teachercomment" ("teacher_id");

-- Index: fees_feerecord_fee_type_id_7d0192af
CREATE INDEX IF NOT EXISTS "fees_feerecord_fee_type_id_7d0192af" ON "fees_feerecord" ("fee_type_id");

-- Index: fees_feerecord_learner_id_2db76245
CREATE INDEX IF NOT EXISTS "fees_feerecord_learner_id_2db76245" ON "fees_feerecord" ("learner_id");

-- Index: learners_classlevel_class_representative_female_id_77d75dd5
CREATE INDEX IF NOT EXISTS "learners_classlevel_class_representative_female_id_77d75dd5" ON "learners_classlevel" ("class_representative_female_id");

-- Index: learners_classlevel_class_representative_male_id_a1f26373
CREATE INDEX IF NOT EXISTS "learners_classlevel_class_representative_male_id_a1f26373" ON "learners_classlevel" ("class_representative_male_id");

-- Index: learners_classlevel_class_teacher_id_dc608b97
CREATE INDEX IF NOT EXISTS "learners_classlevel_class_teacher_id_dc608b97" ON "learners_classlevel" ("class_teacher_id");

-- Index: learners_feesmodel_learner_id_id_700b07a5
CREATE INDEX IF NOT EXISTS "learners_feesmodel_learner_id_id_700b07a5" ON "learners_feesmodel" ("learner_id_id");

-- Index: learners_learnerregister_grade_id_5ba4cf3a
CREATE INDEX IF NOT EXISTS "learners_learnerregister_grade_id_5ba4cf3a" ON "learners_learnerregister" ("grade_id");

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
