/* overlap -- calculate the overlap between nodes
   Overlap is the intersect between the values of two nodes. Expects a
   table with two columns of IDs. Each column represents a node of a
   single type and each row indicates a graph edge.

   So the overlap is the number of common nodes in a bipartisian graph
   between nodes of one type.

   Requires the outer nodes column to be sorted in order to find
   highest ID and to reduce number of calculations (take advantage of
   symmetry).
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

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

/* Return first unsorted edge, or n_edges if fully sorted*/
int is_sorted(int *primary_nodes, int n_edges)
{
  for (int i = 0; i < (n_edges - 1); i++) {
    if (primary_nodes[i + 1] < primary_nodes[i]) {
      return (i + 1);
    }
  }
  return n_edges;
}

/* Find initial edge for each node. */
int find_nodes(int *primary_nodes, int n_edges, int *indices)
{
  int node_idx = 0;
  int node_val = -1;
  for (int edge_idx = 0; edge_idx < n_edges; edge_idx++) {
    if (primary_nodes[edge_idx] != node_val) {
      indices[node_idx] = edge_idx;
      node_val = primary_nodes[edge_idx];
      node_idx++;
    }
  }
  indices[node_idx] = n_edges;

  return node_idx;
}

int main(int argc, char **argv)
{
  int primary_column = 0;
  int secondary_column = 1;
  char delim = '\t';
  int option;
  while ((option = getopt(argc, argv, "k:d:")) != -1) {
    switch (option) {
    case 'k':
      primary_column = atoi(optarg) - 1;
      if ((primary_column != 0) && (primary_column != 1)) {
        fprintf(stderr, "Error: %s.\n\n%s%d.\n",
                "primary column must be 1 or 2",
                "Recieved \"-k \".", primary_column + 1);
        return EXIT_FAILURE;
      }
      secondary_column = !primary_column;
      break;
    case 'd':
      delim = optarg[0];
      break;
    case '?':
      if (optopt == 'k') {
        fprintf(stderr, "Option -k requires an argument.\n");
      } else {
        fprintf(stderr, "Option -%c unknown.\n", optopt);
      }
      return EXIT_FAILURE;
    default:
      abort();
    }
  }

  if (!(optind < argc)) {
    fprintf(stderr, "Error: no edge file provided\n.");
    return EXIT_FAILURE;
  }

  char *f = argv[optind];

  int n_nodes = 0;
  int n_edges = 0;
  int *edges[] = { NULL, NULL };
  int rs = 0;
  if ((n_edges = read_edge_file(f, delim, edges)) == EXIT_FAILURE) {
    return EXIT_FAILURE;
  } else if ((rs = is_sorted(edges[primary_column], n_edges)) != n_edges) {
    fprintf(stderr, ("Error: primary column is not sorted.\n"
                     "\tFirst unsorted edge on line %d.\n"),
            rs);
    return EXIT_FAILURE;
  }

  /* Guess of number of nodes based on largest node id - smallest node id. */
  n_nodes = edges[primary_column][n_edges - 1] - edges[primary_column][0] + 1;

  int *node_indices = calloc(n_nodes + 1, sizeof * node_indices);
  n_nodes = find_nodes(edges[primary_column], n_edges, node_indices);
  int *overlap = NULL;
  int res = 0;

  #pragma omp parallel for private(overlap, res) schedule(dynamic)
  for (int ni = 0; ni < n_nodes; ni++) {
    overlap = calloc(n_nodes, sizeof * overlap);
    for (int nj = (ni + 1); nj < n_nodes; nj++) {
      for (int ei = node_indices[ni]; ei < node_indices[ni + 1]; ei++) {
        #pragma omp simd reduction(+:res)
        for (int ej = node_indices[nj]; ej < node_indices[nj + 1]; ej++) {
          res += (edges[secondary_column][ei] == edges[secondary_column][ej]);
        }
      }
      overlap[nj] = res;
      res = 0;
    }
    flush_overlap(ni, overlap);
    free(overlap);
  }
  free(edges[0]);
  free(edges[1]);
  free(node_indices);

  return EXIT_SUCCESS;
}
