-- 서울 따릉이 자치구별 이용 현황 분석
-- 사용 테이블: ddareung_db (컬럼: 자치구, 대여소명, 대여건수, 반납건수)
-- 실행 환경: DBeaver

-- 1. 자치구별 대여소 수, 대여건수, 반납건수 집계 (대여건수 상위 10개)
select 자치구, count(대여소명) as 대여소수, sum(대여건수) as 대여건수, sum(반납건수) as 반납건수
from `ddareung_db`
group by 자치구
order by 대여건수 desc
limit 10;

-- 2. 같은 집계에서 대여건수 하위 10개 (정렬 방향만 오름차순으로 변경)
select 자치구, count(대여소명) as 대여소수, sum(대여건수) as 대여건수, sum(반납건수) as 반납건수
from `ddareung_db`
group by 자치구
order by 대여건수 asc
limit 10;

-- 3. 대여소당 대여건수 (CTE로 자치구별 집계를 먼저 만든 뒤 계산)
with gu as (
    select 자치구, count(대여소명) as 대여소수, sum(대여건수) as 대여건수
    from `ddareung_db`
    group by 자치구
)
select 자치구, 대여소수, 대여건수,
       round(대여건수 * 1.0 / 대여소수, 1) as 대여소당_대여건수
from gu
order by 대여소당_대여건수 desc;

-- 4. 대여소 수는 평균보다 많은데 대여소당 대여건수는 평균보다 낮은 자치구 (서브쿼리)
with gu as (
    select 자치구, count(대여소명) as 대여소수, sum(대여건수) as 대여건수
    from `ddareung_db`
    group by 자치구
),
per as (
    select 자치구, 대여소수, 대여건수,
           round(대여건수 * 1.0 / 대여소수, 1) as 대여소당_대여건수
    from gu
)
select 자치구, 대여소수, 대여소당_대여건수
from per
where 대여소수 > (select avg(대여소수) from per)
  and 대여소당_대여건수 < (select avg(대여소당_대여건수) from per)
order by 대여소당_대여건수;
