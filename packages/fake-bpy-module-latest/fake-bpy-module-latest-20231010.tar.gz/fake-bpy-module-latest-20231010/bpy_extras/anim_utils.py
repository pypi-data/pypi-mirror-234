import sys
import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")


class BakeOptions:
    pass


class KeyframesCo:
    keyframes_from_fcurve = None
    ''' '''

    def add_paths(self, rna_path, total_indices):
        ''' 

        '''
        pass

    def extend_co_value(self, rna_path, frame, value):
        ''' 

        '''
        pass

    def extend_co_values(self, rna_path, total_indices, frame, values):
        ''' 

        '''
        pass

    def insert_keyframes_into_existing_action(
            self, lookup_fcurves, total_new_keys, action, action_group_name):
        ''' 

        '''
        pass

    def insert_keyframes_into_new_action(self, total_new_keys, action,
                                         action_group_name):
        ''' 

        '''
        pass


def bake_action(obj: 'bpy.types.Object', *,
                action: typing.Optional['bpy.types.Action'], frames: int,
                bake_o) -> 'bpy.types.Action':
    ''' 

    :param obj: Object to bake.
    :type obj: 'bpy.types.Object'
    :param action: An action to bake the data into, or None for a new action to be created.
    :type action: typing.Optional['bpy.types.Action']
    :param frames: Frames to bake.
    :type frames: int
    :rtype: 'bpy.types.Action'
    :return: an action or None
    '''

    pass


def bake_action_iter(obj: 'bpy.types.Object', *,
                     action: typing.Optional['bpy.types.Action'],
                     bake_o) -> 'bpy.types.Action':
    ''' An coroutine that bakes action for a single object.

    :param obj: Object to bake.
    :type obj: 'bpy.types.Object'
    :param action: An action to bake the data into, or None for a new action to be created.
    :type action: typing.Optional['bpy.types.Action']
    :param bake_options: Boolean options of what to include into the action bake.
    :type bake_options: typing.Any
    :rtype: 'bpy.types.Action'
    :return: an action or None
    '''

    pass


def bake_action_objects(object_action_pairs, *, frames: int,
                        bake_o) -> typing.Sequence['bpy.types.Action']:
    ''' A version of :func:`bake_action_objects_iter` that takes frames and returns the output.

    :param frames: Frames to bake.
    :type frames: int
    :rtype: typing.Sequence['bpy.types.Action']
    :return: A sequence of Action or None types (aligned with `object_action_pairs`)
    '''

    pass


def bake_action_objects_iter(
        object_action_pairs: typing.
        Union['bpy.types.Action', 'bpy.types.Sequence', 'bpy.types.Object'],
        bake_o):
    ''' An coroutine that bakes actions for multiple objects.

    :param object_action_pairs: Sequence of object action tuples, action is the destination for the baked data. When None a new action will be created.
    :type object_action_pairs: typing.Union['bpy.types.Action', 'bpy.types.Sequence', 'bpy.types.Object']
    '''

    pass
