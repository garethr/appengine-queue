from google.appengine.ext import db

class DictProperty(db.Property):
  """A property that stores a dict of things. """

  def __init__(self, verbose_name=None, default=None, **kwds):
    """Construct ListProperty.

    Args:
      item_type: Type for the list items; must be one of the allowed property
        types.
      verbose_name: Optional verbose name.
      default: Optional default value; if omitted, an empty list is used.
      **kwds: Optional additional keyword arguments, passed to base class.

    Note that the only permissible value for 'required' is True.
    """
    if 'required' in kwds and kwds['required'] is not True:
      raise ValueError('Dict values must be required')
    if default is None:
      default = {}
    super(DictProperty, self).__init__(verbose_name,
                                       required=True,
                                       default=default,
                                       **kwds)
  def validate(self, value):
    """Validate dict.

    Returns:
      A valid value.

    Raises:
      BadValueError if property is not a dict whose items are instances of
      the allowed types.
    """
    value = super(DictProperty, self).validate(value)
    if value is not None:
      if not isinstance(value, dict):
        raise BadValueError('Property %s must be a dict' % self.name)

      value = self.validate_dict_contents(value)
    return value

  def validate_dict_contents(self, value):
    """Validates that all items in the list are of supported type.

    Returns:
      The validated list.

    Raises:
      BadValueError if the list has items are not instances of the
      supported type.
    """
    for k in value:
      if not isinstance(k, db._ALLOWED_PROPERTY_TYPES):
        raise BadValueError('Keys in the %s dict must be of allowed type' % self.name)
      if not isinstance(value[k], db._ALLOWED_PROPERTY_TYPES):
        raise BadValueError('Items in the %s dict must be of an allowed type' % self.name)
    return value

  def empty(self, value):
    """Is dict property empty.

    {} is not an empty value.

    Returns:
      True if value is None, else false.
    """
    return value is None

  data_type = dict

  def default_value(self):
    """Default value for dict.

    Because the property supplied to 'default' is a static value,
    that value must be shallow copied to prevent all fields with
    default values from sharing the same instance.

    Returns:
      Copy of the default value.
    """
    return dict(super(DictProperty, self).default_value())

  def get_value_for_datastore(self, model_instance):
    """Get value from property to send to datastore.

    Returns:
      validated list appropriate to save in the datastore.
    """
    value = self.validate(super(DictProperty, self).get_value_for_datastore(model_instance))
    result = []
    for k in value:
      result.append(k)
      result.append(value[k])
    return result

  def make_value_from_datastore(self, value):
    if value is None:
      return None
    result = {}
    for i in xrange(0, len(value), 2):
      result[value[i]] = value[i+1]
    return result