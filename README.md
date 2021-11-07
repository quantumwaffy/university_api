# University api service
### Description
The api service supports CRUD for all objects such as Auditorium, Lecture, Group, Student and Schedule. Implemented 
sending emails every evening at 8:30pm (Sunday, Monday, Tuesday, Wednesday, Thursday) for all students who have a 
lecture schedule tomorrow. Implemented a endpoint to get the schedule for a selected date for a specific group. 
The service architecture is easily expandable in the future.

### Quickstart
##### Clone the repository:
```console
git clone https://github.com/quantumwaffy/university_api.git
```
##### Go to the downloaded project:
```console
cd university_api
```
##### Up docker container:
```console
docker-compose up -d
```
After the container is up, the application will run on localhost:8000/api/.
#### The following urls are available for making requests:
<i>Authorization is required to create, edit or delete any entries.<i>
<ul><b>auditorium/list/</b> -get info about all audiences</ul>
<ul><b>auditorium/detail/[auditorium_id]/</b> -get, update, delete info about selected audience</ul>
<ul><b>auditorium/create/</b> -create new auditorium</ul>
<ul><b>group/list/</b> -get info about all groups</ul>
<ul><b>group/detail/[group_id]/</b> -get, update, delete info about selected group</ul>
<ul><b>group/create/</b> -create new group</ul>
<ul><b>student/list/</b> -get info about all students</ul>
<ul><b>student/detail/[student_id]/</b> -get, update, delete info about selected student</ul>
<ul><b>student/create/</b> -create new student</ul>
<ul><b>lecture/list/</b> -get info about all lectures</ul>
<ul><b>lecture/detail/[lecture_id]/</b> -get, update, delete info about selected lecture</ul>
<ul><b>lecture/create/</b> -create new lecture</ul>
<ul><b>schedule/list/</b> -get info about all schedule entries</ul>
<ul><b>schedule/detail/[schedule_id]/</b> -get, update, delete info about selected schedule</ul>
<ul><b>schedule/create/</b> -create new schedule entry</ul>
<ul><b>get-date-schedule/</b> -POST request with the required parameters of date in the format Y-m-d (schedule_date) 
and group name (schedule_group) to get the schedule for the selected day for the specified group</ul>

