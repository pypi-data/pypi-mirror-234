#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <numpy/ndarraytypes.h>
#include <numpy/ufuncobject.h>

/* A value assumed to be larger than needed.  Neighbors will likely
   mean either author's publications or publication's authors. If
   mores needed can dynamically re calloc. */
#define MAX_NEIGHBORS 500

/* Move forward in file one line. */
char fskipl(FILE *fptr)
{
  char c = '\0';
  while (((c = getc(fptr)) != '\n') && (c != EOF));

  return c;
}

int fget_cols(FILE *fptr, char delim, int *col1, int *col2)
{
  char c = '\0';
  char buff[20];
  int i = 0;
  int coli = 0;

  while ((c = getc(fptr)) != '\n' && c != EOF) {
    if (c == delim) {
      buff[i] = '\0';
      *col1 = atoi(buff);
      coli++;
      i = 0;
    } else {
      buff[i] = c;
      i++;
    }
  }

  buff[i] = '\0';
  *col2 = atoi(buff);
  coli++;

  return coli;
}

void skip_header(FILE *fptr, char delim)
{
  int buff[2];
  int pos = ftell(fptr);
  while (fget_cols(fptr, delim, &buff[0], &buff[1]) == 2) {
    if ((buff[0] > 0) || (buff[1] > 0)) {
      break;
    }
    pos = ftell(fptr);
  }
  fseek(fptr, pos, SEEK_SET);
}

int read_edge_file(char *f, char delim, int *edges[2])
{
  FILE *fptr;
  if (!(fptr = fopen(f, "r"))) {
    fprintf(stderr, "Error: could not open file %s\n", f);
    return EXIT_FAILURE;
  }

  char c = '\0';
  int n_edges = 0;
  skip_header(fptr, delim);
  while ((c = fskipl(fptr)) != EOF) n_edges++;

  edges[0] = malloc(n_edges * sizeof * edges[0]);
  edges[1] = malloc(n_edges * sizeof * edges[1]);

  rewind(fptr);
  skip_header(fptr, delim);
  int i = 0;
  while ((fget_cols(fptr, delim, &edges[0][i], &edges[1][i])) == 2) i++;

  fclose(fptr);

  if (i != n_edges) {
    fprintf(stderr,
            ("Error: could not read all edges in edge file."
             "Ensure all lines after the header are of the form %%d%c%%d."),
            delim);
    return EXIT_FAILURE;
  }

  return n_edges;
}

int is_sorted(int *primary_nodes, int n_edges)
{
  for (int i = 0; i < (n_edges - 1); i++) {
    if (primary_nodes[i + 1] < primary_nodes[i]) {
      return (i + 1);
    }
  }
  return n_edges;
}

PyMODINIT_FUNC initSubgraph(void)
{
  (void)Py_InitModule("subgraph", mymethods);
  import_array();
}

/* static PyObject *method_neighbors(PyObject *self, PyObject *args) */
/* { */
/*   char *filename = NULL; */
/*   int id = 0; */
/*   int col = 0; */
/*   char delim = '\t'; */
/*   int neighbors[MAX_NEIGHBORS]; */

/*   int n_edges = 0; */
/*   // ensure int is large enough, 16bit should be too small for PMIDs, additionally consider unsigned. */
/*   int *edges[] = { NULL, NULL }; */
/*   int rs = 0; */
/*   if ((n_edges = read_edge_file(filename, delim, edges)) == EXIT_FAILURE) { */
/*     /\* return EXIT_FAILURE; *\/ */
/*   } else if ((rs = is_sorted(edges[col], n_edges)) != n_edges) { */
/*     fprintf(stderr, ("Error: primary column is not sorted.\n" */
/*                      "\tFirst unsorted edge on line %d.\n"), */
/*             rs); */
/*     /\* return EXIT_FAILURE; *\/ */
/*   } */
/* } */
