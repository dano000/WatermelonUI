#
#
#
#
#


# import the inspect_checkpoint library
from tensorflow.python.tools import inspect_checkpoint as chkp

# print all tensors in checkpoint file
chkp.print_tensors_in_checkpoint_file("./model.ckpt", tensor_name='', all_tensors=True)

