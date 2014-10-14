%module JDTime
%{

typedef struct {
  int year;
  int month;
  int day;
  int hour;
  int minute;
  double second; } JDTime;

%}

typedef struct {
  int year;
  int month;
  int day;
  int hour;
  int minute;
  double second; } JDTime;

extern double date2jd( JDTime *jdt );

extern void jd2date( double jd , JDTime *jdt );

extern double monthlystep( void );
