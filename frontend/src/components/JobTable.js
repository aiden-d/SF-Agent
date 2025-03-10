import React, { useState } from "react";
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  Chip,
  CircularProgress,
  Typography,
  Tooltip,
} from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import LinkIcon from "@mui/icons-material/Link";

function JobTable({ jobs, loading }) {
  const [orderBy, setOrderBy] = useState("date_found");
  const [order, setOrder] = useState("desc");

  // Handle request sort
  const handleRequestSort = (property) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  // Sort function
  const sortedJobs = React.useMemo(() => {
    if (!jobs || jobs.length === 0) return [];

    return [...jobs].sort((a, b) => {
      let valueA = a[orderBy];
      let valueB = b[orderBy];

      // Handle dates
      if (orderBy === "date_posted" || orderBy === "date_found") {
        valueA = new Date(valueA);
        valueB = new Date(valueB);
      }

      if (valueA < valueB) {
        return order === "asc" ? -1 : 1;
      }
      if (valueA > valueB) {
        return order === "asc" ? 1 : -1;
      }
      return 0;
    });
  }, [jobs, order, orderBy]);

  // Format date
  const formatDate = (dateString) => {
    if (!dateString) return "N/A";
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  // Create sortable table header
  const createSortHandler = (property) => () => {
    handleRequestSort(property);
  };

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!jobs || jobs.length === 0) {
    return (
      <Paper sx={{ p: 3, textAlign: "center" }}>
        <Typography variant="h6">No jobs found yet</Typography>
        <Typography variant="body2" color="text.secondary">
          Start the agent to begin crawling for jobs with visa sponsorship.
        </Typography>
      </Paper>
    );
  }

  return (
    <Paper sx={{ width: "100%", mb: 2 }}>
      <TableContainer>
        <Table sx={{ minWidth: 750 }} aria-labelledby="jobsTable">
          <TableHead>
            <TableRow>
              <TableCell>
                <TableSortLabel
                  active={orderBy === "title"}
                  direction={orderBy === "title" ? order : "asc"}
                  onClick={createSortHandler("title")}
                >
                  Job Title
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === "company"}
                  direction={orderBy === "company" ? order : "asc"}
                  onClick={createSortHandler("company")}
                >
                  Company
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === "location"}
                  direction={orderBy === "location" ? order : "asc"}
                  onClick={createSortHandler("location")}
                >
                  Location
                </TableSortLabel>
              </TableCell>
              <TableCell>Visa Sponsorship</TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === "date_posted"}
                  direction={orderBy === "date_posted" ? order : "asc"}
                  onClick={createSortHandler("date_posted")}
                >
                  Date Posted
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === "date_found"}
                  direction={orderBy === "date_found" ? order : "asc"}
                  onClick={createSortHandler("date_found")}
                >
                  Date Found
                </TableSortLabel>
              </TableCell>
              <TableCell>Link</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {sortedJobs.map((job) => (
              <TableRow
                key={job.id}
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  <Tooltip title={job.description}>
                    <Typography variant="body2">{job.title}</Typography>
                  </Tooltip>
                </TableCell>
                <TableCell>{job.company}</TableCell>
                <TableCell>{job.location}</TableCell>
                <TableCell>
                  {job.visa_sponsorship ? (
                    <Chip
                      icon={<CheckCircleIcon />}
                      label="Available"
                      color="success"
                      size="small"
                    />
                  ) : (
                    <Chip label="Unknown" size="small" />
                  )}
                </TableCell>
                <TableCell>{formatDate(job.date_posted)}</TableCell>
                <TableCell>{formatDate(job.date_found)}</TableCell>
                <TableCell>
                  <a href={job.url} target="_blank" rel="noopener noreferrer">
                    <LinkIcon />
                  </a>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}

export default JobTable;
