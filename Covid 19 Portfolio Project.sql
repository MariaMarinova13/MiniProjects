Select *
From PorfolioProject..Covid_Deaths$
order by 3,4

Select Location, date, total_cases, new_cases, total_deaths, population
From PorfolioProject..Covid_Deaths$
order by 1,2

-- Comparing Total cases vs Total Deaths

Select Location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
From PorfolioProject..Covid_Deaths$
order by 1,2

Select Location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
From PorfolioProject..Covid_Deaths$
Where Location='Bulgaria'
order by 1,2

-- Total Cases vs Population

Select Location, Population, date, MAX(total_cases) as HighestInfectionCount, MAX(total_cases/population)*100 as PercentPopulationInfected
From PorfolioProject..Covid_Deaths$
Group by Location, Population, date
order by PercentPopulationInfected desc

--Countries with highest infection rate compared to population
Select Location, Population, MAX(total_cases) as HighestInfectionCount, MAX((total_cases/population))*100 as PercentPopulationInfected
From PorfolioProject..Covid_Deaths$
Group by Location, Population
order by PercentPopulationInfected desc

-- Countries with the highest death count per population

Select Location, MAX(cast(Total_deaths as int)) as TotalDeathCount
From PorfolioProject..Covid_Deaths$
Where continent is not null
Group by Location
order by TotalDeathCount desc

-- Grouping the data by continent in order to see the death count per population

Select location, SUM(cast(new_deaths as int)) as TotalDeathCount
From PorfolioProject..Covid_Deaths$
Where continent is null
and location not in ('World', 'European Union', 'International', 'High income', 'Upper middle income', 'Lower middle income', 'Low income')
Group by location
order by TotalDeathCount desc

-----


-- Global numbers

Select SUM(new_cases) as total_cases, SUM(cast(new_deaths as int)) as total_deaths, SUM(cast(new_deaths as int))/SUM(new_cases)*100 as DeathPercentage
From PorfolioProject..Covid_Deaths$
where continent is not null
--Group by date
order by 1,2

--Percent People Vaccinated

Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(bigint, vac.new_vaccinations)) OVER (Partition by dea.Location Order by dea.location, dea.Date)
as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From PorfolioProject..Covid_Deaths$ dea
Join PorfolioProject..Covid_Vacc$ vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
order by 2,3



--CTE

With PopvsVac (Continent, Location, Date, Population, New_Vaccinations, RollingPeopleVaaccinated)
as
( 
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(bigint, vac.new_vaccinations)) OVER (Partition by dea.Location Order by dea.location, dea.Date)
as RollingPeopleVaccinated
From PorfolioProject..Covid_Deaths$ dea
Join PorfolioProject..Covid_Vacc$ vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
)
Select *, (RollingPeopleVaaccinated/Population)*100
From PopvsVac

--TEMP TABLE

DROP Table if exists #PercentPopulationVaccinated
Create Table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
RollingPeopleVaccinated numeric
)
 
Insert into #PercentPopulationVaccinated
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(bigint, vac.new_vaccinations)) OVER (Partition by dea.Location Order by dea.location, dea.Date)
as RollingPeopleVaccinated
From PorfolioProject..Covid_Deaths$ dea
Join PorfolioProject..Covid_Vacc$ vac
	On dea.location = vac.location
	and dea.date = vac.date
--where dea.continent is not null

Select *, (RollingPeopleVaccinated/Population)
From #PercentPopulationVaccinated

--Creating View to store data for vizualizations

Create View PercentPopulationVaccinated as
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(bigint, vac.new_vaccinations)) OVER (Partition by dea.Location Order by dea.location, dea.Date)
as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From PorfolioProject..Covid_Deaths$ dea
Join PorfolioProject..Covid_Vacc$ vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2,3

Select *
From PercentPopulationVaccinated

-- Percent of people fully vaccinated in each country

Select *
From PorfolioProject..Covid_Vacc$
where location='Bulgaria'
order by 3,4

---

DROP Table if exists #PercentFullyVaccinated
Create Table #PercentFullyVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Population numeric,
PeopleFullyVacc numeric
)
Insert into #PercentFullyVaccinated
Select dea.continent, dea.location, dea.population
, MAX(CONVERT(bigint, vac.people_fully_vaccinated)) as PeopleFullyVacc
From PorfolioProject..Covid_Deaths$ dea
Join PorfolioProject..Covid_Vacc$ vac
	On dea.location = vac.location
where dea.continent is not null
--order by 2,3
group by  dea.location, dea.continent, dea.population

Select *, (PeopleFullyVacc/Population)*100 as PercentPeopleFullyVacc
From #PercentFullyVaccinated

--Percent hospitalized patients

Select continent, location, date, total_cases, new_cases, hosp_patients, (hosp_patients/total_cases)*100 as PercentHospPatients
From PorfolioProject..Covid_Deaths$
Where continent is not null
and location='Bulgaria'
order by 2,3

-- What is the percentage of people infected in the most populated countries in the world.
DROP Table if exists #Populationdensity
Create Table #Populationdensity
(
Continent nvarchar(255),
Location nvarchar(255),
NumberOfCases float, 
PopulationDensity numeric
)
Insert into #Populationdensity
Select dea.continent, dea.location, MAX((dea.total_cases)/dea.population)*100 as NumberOfCases
, vac.population_density as PopulationDensity
From PorfolioProject..Covid_Deaths$ dea
Join PorfolioProject..Covid_Vacc$ vac
	On dea.location = vac.location
where dea.continent is not null
--order by 2,3
group by  dea.location, dea.continent, vac.population_density

Select *
From #Populationdensity

----Which contries have made the most tests as per population

DROP Table if exists #TotalTests
Create Table #TotalTests
(
Continent nvarchar(255),
Location nvarchar(255),
Population numeric,
TotalTests numeric
)
Insert into #TotalTests
Select dea.continent, dea.location, dea.population
, MAX(vac.total_tests) as TotalTests
From PorfolioProject..Covid_Deaths$ dea
Join PorfolioProject..Covid_Vacc$ vac
	On dea.location = vac.location
where dea.continent is not null
--order by 2,3
group by  dea.location, dea.continent, dea.population

Select *, (TotalTests/Population) as TestsVsPopulation
From #TotalTests

