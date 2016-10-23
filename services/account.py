import utils
import pydash as _

'''
Get account information based on provided user_id
@param {int} user_id
@returns {dict|None}
'''
def get_user(user_id):
  
  result_list = utils.db.relational_query(
    """
    SELECT 
      username, hp, xp, 
      users_items.id AS item_id, 
      users_items.name AS item_name, 
      users_items.description AS item_description, 
      users_items.quantity AS item_quantity
    FROM users 
      JOIN (
        SELECT id, users_items.user_id AS user_id, 
          name, description, quantity 
        FROM items 
          JOIN users_items ON items.id=users_items.item_id
        WHERE users_items.user_id=%s
      ) AS users_items ON users.id=users_items.user_id
    ;
    """,
    [user_id]
  )
  
  if (len(result_list) == 0):
    return None
  
  inventory_list = _.map(result_list, lambda _tuple: {
    id: _tuple[3],
    name: _tuple[4],
    description: _tuple[5],
    quantity: _tuple[6]
  })
  
  return {
    username: result_list[0][0], 
    hp: result_list[0][1], 
    xp: result_list[0][2], 
    inventory: inventory_list
  }


'''
Updates user information
@param {int} user_id
@returns {boolean} TRUE on success, FALSE on failure
'''
def update_user(user_id, updated_user_dict={}):
  
  username = updated_user_dict.get("username")
  hp = updated_user_dict.get("hp")
  xp = updated_user_dict.get("xp")
  inventory_list = updated_user_dict.get("inventory", [])
  
  if username is not None and isinstance(username, basestring):
    utils.db.relational_query(
      """
      UPDATE users 
      SET username=%s;
      """,
      [username]
    )
  if hp is not None and isinstance(hp, int):
    utils.db.relational_query(
      """
      UPDATE users
      SET hp=%s;
      """,
      [hp]
    )
  if xp is not None and isinstance(xp, int):
    utils.db.relational_query(
      """
      UPDATE users 
      SET xp=%s;
      """,
      [xp]
    )
  
  def update_items(item_id, item_quantity):
    utils.db.relational_query(
      """
      INSERT INTO users_items (user_id, item_id, quantity) 
      VALUES (%s, %s, %s)
      ON CONFLICT (user_id, item_id) DO UPDATE 
        SET quantity=%s
      """,
      [user_id, item_id, item_quantity, item_quantity]
    )
  for item in inventory_list:
    item_id = item.get("id")
    item_quantity = item.get("quantity")
    update_items(item_id, item_quantity)
  
  return True
