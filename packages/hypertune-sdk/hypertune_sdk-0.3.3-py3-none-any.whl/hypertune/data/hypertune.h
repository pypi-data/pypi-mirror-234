typedef enum NodeIteratorState {
  MaybeMore,
  Consumed,
} NodeIteratorState;

typedef enum NodeResultType {
  String,
  Enum,
  Int,
  Float,
  Bool,
  Object,
  Void,
  Unknown,
} NodeResultType;

typedef struct SizedString {
  uint8_t bytes[255];
  uint8_t length;
} SizedString;

typedef struct NodeResult {
  uint32_t id;
  enum NodeResultType type;
  struct SizedString object_type_name;
  struct SizedString value;
} NodeResult;

typedef struct NodeIteratorResult {
  uint32_t id;
} NodeIteratorResult;

typedef struct NodeIteratorNextResult {
  enum NodeIteratorState state;
  struct NodeResult node;
} NodeIteratorNextResult;

/**
 * # Safety
 *
 * This is unsafe because we accept raw pointers to strings. Callers must
 * ensure they pass in proper NULL terminated C strings.
 */
struct NodeResult initialize(const char *variable_values,
                             const char *fallback_init_data,
                             const char *token,
                             const char *query_code,
                             const char *query,
                             const char *language,
                             const char *endpoints);

/**
 * # Safety
 *
 * This is unsafe because we accept raw pointers to strings. Callers must
 * ensure they pass in proper NULL terminated C strings.
 */
struct NodeResult node_get_field(uint32_t node_handle, const char *field, const char *arguments);

struct NodeIteratorResult node_get_items(uint32_t node_handle);

struct NodeIteratorNextResult node_iterator_next(uint32_t iterator_handle);

/**
 * # Safety
 *
 * This is unsafe because we accept raw pointers to strings. Callers must
 * ensure they pass in proper NULL terminated C strings.
 */
struct SizedString node_evaluate(uint32_t node_handle);
