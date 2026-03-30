# Requirements Specification — Stack Overflow Trends Project

## 1. Functional Requirements

### 1.1 Data Source
- The system shall retrieve Stack Overflow question data programmatically.
- Data sources may include Stack Exchange API or Stack Exchange Data Explorer (SEDE).
- The data shall represent monthly question counts.

### 1.2 Date Range
- The system shall include data from January 2008 to December 2024.

### 1.3 Data Processing
- The system shall aggregate data into monthly counts.
- The system shall compute a 12-month rolling average.

### 1.4 Visualization
- The system shall generate a time series line chart.
- The chart shall include:
  - Monthly question counts
  - 12-month rolling average

### 1.5 Milestone Overlay
- The system shall overlay AI milestone markers on the plot.
- Milestones include:
  - Transformer (2017)
  - ChatGPT (2022)
  - GPT-4 (2023)
  - Additional milestones if needed

---

## 2. Non-Functional Requirements

### 2.1 Performance
- Data shall be cached locally (e.g., CSV file).
- Repeated runs shall use cached data when available.

### 2.2 Reliability
- The system shall handle API/network errors gracefully.
- Retry logic shall be implemented for failed requests.

### 2.3 Usability
- The chart shall include:
  - Clear axis labels
  - Title
  - Legend
- The output shall be saved as a PNG image.

---

## 3. Acceptance Criteria

### 3.1 Data Fetching
- Data is successfully fetched or loaded from cache.
- Output format: pandas DataFrame with:
  - year_month (datetime)
  - question_count (int)

### 3.2 Data Processing
- Monthly aggregation is correct.
- Rolling average is correctly computed.

### 3.3 Visualization
- Chart is generated without errors.
- Both lines (raw and rolling average) are visible.

### 3.4 Milestones
- Milestones appear at correct dates.
- Labels are readable and properly positioned.

### 3.5 Output
- File `so_trends.png` is created successfully.