from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.join(Path(os.path.dirname(os.path.abspath(__file__))).resolve()))

from Types.Requests import Options, Buildings, Rooms, Terms, Groups, Subjects, Courses, Course_Instructor, Course_Sections, Offerings, Instructors, Sections, Coverages, Error
from Types.Facility import Building, Room
from Types.Term import Term
from Types.Academic import Group, Subject
from Types.Course import Course, Offering, Section
from Types.Faculty import Instructor
from Types.Coverage import Coverage
from methods.fetch import _fetch

import asyncio


api_base = "https://spire-api.melanson.dev"

HEADERS = {
    "Content-Type": "application/json",
}
    
class _buildings:
    endpoint = "/buildings"

    async def getBuildings(
        self,
        options: Options.PageSearch = {}
    ) -> Buildings:
        return await _fetch(
            dataclassType=Buildings,
            options={
                "url": f"{api_base}{self.endpoint}",
                "headers": HEADERS,
                "params": options
            }
        )
    
    async def getBuilding(
        self,
        id: str,
        options: Options.Search = {}
    ) -> Building | Error:
        return await _fetch(
            dataclassType=Building,
            options={
                "url": f"{api_base}{self.endpoint}/{id}",
                "headers": HEADERS,
                "params": options
            }
        )
    
    async def getTotalBuildings(
        self,
        options: Options.Search = {}
    ) -> list[Buildings]:
        buildingList = []
        page = 1
        last = False

        while not last:
            options.update({"page": page})
            buildings = await _fetch(
                dataclassType=Buildings,
                options={
                    "url": f"{api_base}{self.endpoint}",
                    "headers": HEADERS,
                    "params": options
                }
            )
            buildingList += buildings.results
            if buildings.next is None:
                last = True
            else:
                page += 1
        return buildingList

class _rooms:
    endpoint = "/building-rooms"

    async def getRooms(
        self,
        options: Options.Page = {}
    ) -> Rooms:
        return await _fetch(
            dataclassType=Rooms,
            options={
                "url": f"{api_base}{self.endpoint}",
                "headers": HEADERS,
                "params": options
            }
        )
    
    async def getRoom(
        self,
        id: str
    ) -> Room | Error:
        return await _fetch(
            dataclassType=Room,
            options={
                "url": f"{api_base}{self.endpoint}/{id}",
                "headers": HEADERS,
                "params": {
                    "id": id
                }
            }
        )
    
    async def getTotalRooms(
        self
    ) -> list[Room]:
        roomList = []
        page = 1
        last = False

        while not last:
            rooms = await _fetch(
                dataclassType=Rooms,
                options={
                    "url": f"{api_base}{self.endpoint}",
                    "headers": HEADERS,
                    "params": {
                        "page": page
                    }
                }
            )
            roomList += rooms.results
            if rooms.next is None:
                last = True
            else:
                page += 1
        return roomList

class _terms:
    endpoint = "/terms"

    async def getTerms(
        self,
        options: Options.Page = {}
    ) -> Terms:
        return await _fetch(
            dataclassType=Terms,
            options={
                "url": f"{api_base}{self.endpoint}",
                "headers": HEADERS,
                "params": options
            }
        )
    
    async def getTerm(
        self,
        id: str
    ) -> Term | Error:
        return await _fetch(
            dataclassType=Term,
            options={
                "url": f"{api_base}{self.endpoint}/{id}",
                "headers": HEADERS,
                "params": {
                    "id": id
                }
            }
        )
    
    async def getTotalTerms(
        self
    ) -> list[Term]:
        termList = []
        page = 1
        last = False

        while not last:
            terms = await _fetch(
                dataclassType=Terms,
                options={
                    "url": f"{api_base}{self.endpoint}",
                    "headers": HEADERS,
                    "params": {
                        "page": page
                    }
                }
            )
            termList += terms.results
            if terms.next is None:
                last = True
            else:
                page += 1
        return termList

class _groups:
    endpoint = "/academic-groups"

    async def getGroups(
        self,
        options: Options.PageSearch = {}
    ) -> Groups:
        return await _fetch(
            dataclassType=Groups,
            options={
                "url": f"{api_base}{self.endpoint}",
                "headers": HEADERS,
                "params": options
            }
        )

    async def getGroup(
        self,
        id: str
    ) -> Group | Error:
        return await _fetch(
            dataclassType=Group,
            options={
                "url": f"{api_base}{self.endpoint}/{id}",
                "headers": HEADERS,
                "params": {
                    "id": id
                }
            }
        )
    
    async def getTotalGroups(
        self
    ) -> list[Group]:
        groupList = []
        page = 1
        last = False

        while not last:
            groups = await _fetch(
                dataclassType=Groups,
                options={
                    "url": f"{api_base}{self.endpoint}",
                    "headers": HEADERS,
                    "params": {
                        "page": page
                    }
                }
            )
            groupList += groups.results
            if groups.next is None:
                last = True
            else:
                page += 1
        return groupList

class _subjects:
    endpoint = "/subjects"

    async def getSubjects(
        self,
        options: Options.PageSearch = {}
    ) -> Subjects:
        return await _fetch(
            dataclassType=Subjects,
            options={
                "url": f"{api_base}{self.endpoint}",
                "headers": HEADERS,
                "params": options
            }
        )

    async def getSubject(
        self,
        id: str,
        params: Options.Search = {}
    ) -> Subject | Error:
        params.update({"id": id})
        return await _fetch(
            dataclassType=Subject,
            options={
                "url": f"{api_base}{self.endpoint}/{id}",
                "headers": HEADERS,
                "params": params
            }
        )
    
    async def getTotalSubjects(
        self
    ) -> list[Subject]:
        subjectList = []
        page = 1
        last = False

        while not last:
            subjects = await _fetch(
                dataclassType=Subjects,
                options={
                    "url": f"{api_base}{self.endpoint}",
                    "headers": HEADERS,
                    "params": {
                        "page": page
                    }
                }
            )
            subjectList += subjects.results
            if subjects.next is None:
                last = True
            else:
                page += 1
        return subjectList

class _courses:
    endpoint = "/courses"

    async def getCourses(
        self,
        options: Options.PageSearch = {}
    ) -> Courses:
        return await _fetch(
            dataclassType=Courses,
            options={
                "url": f"{api_base}{self.endpoint}",
                "headers": HEADERS,
                "params": options
            }
        )
    
    async def getCourse(
        self,
        id: str,
        options: Options.Search = {}
    ) -> Course | Error:
        return await _fetch(
            dataclassType=Course,
            options={
                "url": f"{api_base}{self.endpoint}/{id}",
                "headers": HEADERS,
                "params": options
            }
        )
    
    async def getCourseInstructor(
        self,
        id: str
    ) -> list[Course_Instructor] | Error:
        return await _fetch(
            dataclassType=Course_Instructor,
            options={
                "url": f"{api_base}{self.endpoint}/{id}/instructors",
                "headers": HEADERS,
                "params": {
                    "id": id
                }
            }
        )
    
    async def getCourseSection(
        self,
        id: str
    ) -> Section | Error:
        return await _fetch(
            dataclassType=Course_Sections,
            options={
                "url": f"{api_base}{self.endpoint}/{id}/sections",
                "headers": HEADERS,
                "params": {
                    "id": id
                }
            }
        )

    async def getTotalCourses(
        self
    ) -> list[Course]:
        courseList = []
        page = 1
        last = False

        while not last:
            courses = await _fetch(
                dataclassType=Courses,
                options={
                    "url": f"{api_base}{self.endpoint}",
                    "headers": HEADERS,
                    "params": {
                        "page": page
                    }
                }
            )
            courseList += courses.results
            if courses.next is None:
                last = True
            else:
                page += 1
        return courseList

class _offerings:
    endpoint = "/course-offerings"

    async def getOfferings(
        self,
        options: Options.Page = {}
    ) -> Offerings:
        return await _fetch(
            dataclassType=Offerings,
            options={
                "url": f"{api_base}{self.endpoint}",
                "headers": HEADERS,
                "params": options
            }
        )
    
    async def getOffering(
        self,
        id: str
    ) -> Offering | Error:
        return await _fetch(
            dataclassType=Offering,
            options={
                "url": f"{api_base}{self.endpoint}/{id}",
                "headers": HEADERS,
                "params": {
                    "id": id
                }
            }
        )
    
    async def getTotalOfferings(
        self
    ) -> list[Offering]:
        offeringList = []
        page = 1
        last = False

        while not last:
            offerings = await _fetch(
                dataclassType=Offerings,
                options={
                    "url": f"{api_base}{self.endpoint}",
                    "headers": HEADERS,
                    "params": {
                        "page": page
                    }
                }
            )
            offeringList += offerings.results
            if offerings.next is None:
                last = True
            else:
                page += 1
        return offeringList

class _instructors:
    endpoint = "/instructors"

    async def getInstructors(
        self,
        options: Options.PageSearch = {}
    ) -> Instructors:
        return await _fetch(
            dataclassType=Instructors,
            options={
                "url": f"{api_base}{self.endpoint}",
                "headers": HEADERS,
                "params": options
            }
        )
    
    async def getInstructor(
        self,
        id: str,
        options: Options.Search = {}
    ) -> Instructor | Error:
        return await _fetch(
            dataclassType=Instructor,
            options={
                "url": f"{api_base}{self.endpoint}/{id}",
                "headers": HEADERS,
                "params": options
            }
        )
    
    async def getTotalInstructors(
        self
    ) -> list[Instructor]:
        instructorList = []
        page = 1
        last = False

        while not last:
            instructors = await _fetch(
                dataclassType=Instructors,
                options={
                    "url": f"{api_base}{self.endpoint}",
                    "headers": HEADERS,
                    "params": {
                        "page": page
                    }
                }
            )
            instructorList += instructors.results
            if instructors.next is None:
                last = True
            else:
                page += 1
        return instructorList
    
    async def getInstructorSection(
        self,
        id: str
    ) -> Course_Sections | Error:
        return await _fetch(
            dataclassType=Course_Sections,
            options={
                "url": f"{api_base}{self.endpoint}/{id}/sections",
                "headers": HEADERS,
                "params": {
                    "id": id
                }
            }
        )

class _sections:
    endpoint = "/sections"

    async def getSections(
        self,
        options: Options.Page = {}
    ) -> Sections:
        return await _fetch(
            dataclassType=Sections,
            options={
                "url": f"{api_base}{self.endpoint}",
                "headers": HEADERS,
                "params": options
            }
        )
    
    async def getSection(
        self,
        id: str
    ) -> Section | Error:
        return await _fetch(
            dataclassType=Section,
            options={
                "url": f"{api_base}{self.endpoint}/{id}",
                "headers": HEADERS,
                "params": {}
            }
        )
    
    async def getTotalSections(
        self
    ) -> list[Section]:
        sectionList = []
        page = 1
        last = False

        while not last:
            sections = await _fetch(
                dataclassType=Course_Sections,
                options={
                    "url": f"{api_base}{self.endpoint}",
                    "headers": HEADERS,
                    "params": {
                        "page": page
                    }
                }
            )
            sectionList += sections.results
            if sections.next is None:
                last = True
            else:
                page += 1
        return sectionList

class _coverages:
    endpoint = "/coverage"

    async def getCoverages(
        self,
        options: Options.Page = {}
    ) -> Coverages:
        return await _fetch(
            dataclassType=Coverages,
            options={
                "url": f"{api_base}{self.endpoint}",
                "headers": HEADERS,
                "params": options
            }
        )
    
    async def getCoverageTerm(
        self,
        term: str
    ) -> Coverage | Error:
        return await _fetch(
            dataclassType=Coverage,
            options={
                "url": f"{api_base}{self.endpoint}/{term}",
                "headers": HEADERS,
                "params": {}
            }
        )
    
    async def getTotalCoverages(
        self
    ) -> list[Coverage]:
        coverageList = []
        page = 1
        last = False

        while not last:
            coverages = await _fetch(
                dataclassType=Coverages,
                options={
                    "url": f"{api_base}{self.endpoint}",
                    "headers": HEADERS,
                    "params": {
                        "page": page
                    }
                }
            )
            coverageList += coverages.results
            if coverages.next is None:
                last = True
            else:
                page += 1
        return coverageList

class Spire:
    buildings: _buildings = _buildings()
    rooms: _rooms = _rooms()
    terms: _terms = _terms()
    groups: _groups = _groups()
    subjects: _subjects = _subjects()
    courses: _courses = _courses()
    offering: _offerings = _offerings()
    instructor: _instructors = _instructors()
    section: _sections = _sections()
    coverage: _coverages = _coverages()
