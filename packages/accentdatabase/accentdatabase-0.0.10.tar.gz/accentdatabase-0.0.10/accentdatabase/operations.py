from alembic.operations import MigrateOperation, Operations


class DatabaseFunction:
    """
    Class used to create a function within the db

    - define the function::

        from accentdatabase.operations import DatabaseFunction

        my_function = DatabaseFunction(
            "my_function()",
            \"""
            RETURNS trigger AS $trigger$
            BEGIN
               -- trigger logic
            END;
            $trigger$ LANGUAGE plpgsql;
            \""",
        )

    - use within alembic migration::

        def upgrade():
            op.create_fn(my_function)

        def downgrade():
            op.drop_fn(my_function)

    - additionally there is a replace operations for modifications::

        def upgrade():
            op.replace_fn(my_function, replaces="28af9800143f.my_function")

        def downgrade():
            op.replace_fn(my_function, replace_with="28af9800143f.my_function")

    """

    def __init__(self, name: str, sql: str):
        self.name = name
        self.sql = sql


class DatabaseTrigger:
    """
    Class used to create a trigger within the db

    - define the trigger::

        from accentdatabase.operations import DatabaseTrigger

        my_trigger = DatabaseTrigger(
            "my_trigger_name",
            "AFTER INSERT OR UPDATE OR DELETE",
            "table_name",
            "FOR EACH ROW EXECUTE PROCEDURE some_function();",
        )

    - use within alembic migration::

        def upgrade():
            op.create_trg(my_trigger)

        def downgrade():
            op.drop_trg(my_trigger)

    - additionally there is a replace operations for modifications::

        def upgrade():
            op.replace_trg(my_trigger, replaces="28af9800143f.my_trigger")

        def downgrade():
            op.replace_trg(my_trigger, replace_with="28af9800143f.my_trigger")

    """

    def __init__(self, name: str, when: str, on: str, sql: str):
        self.name = name
        self.when = when
        self.on = on
        self.sql = sql


class DatabaseView:
    """
    Class used to create a view within the db

    - define the view::

        from accentdatabase.operations import DatabaseView

        my_view = DatabaseView(
            "my_view",
            \"""
            SELECT * FROM some_table;
            \""",
        )

    - use within alembic migration::

        def upgrade():
            op.create_vw(my_view)

        def downgrade():
            op.drop_vw(my_view)

    - additionally there is a replace operations for modifications::

        def upgrade():
            op.replace_vw(my_view, replaces="28af9800143f.my_view")

        def downgrade():
            op.replace_vw(my_view, replace_with="28af9800143f.my_view")

    """

    def __init__(self, name: str, sql: str):
        self.name = name
        self.sql = sql


class ReversibleOperation(MigrateOperation):
    def __init__(self, target):
        self.target = target

    @classmethod
    def invoke_for_target(cls, operations, target):
        op = cls(target)
        return operations.invoke(op)

    def reverse(self):
        raise NotImplementedError()

    @classmethod
    def _get_object_from_version(cls, operations, ident):
        version, objname = ident.split(".")
        module = operations.get_context().script.get_revision(version).module
        return getattr(module, objname)

    @classmethod
    def replace(cls, operations, target, replaces=None, replace_with=None):
        if replaces:
            old_obj = cls._get_object_from_version(operations, replaces)
            drop_old = cls(old_obj).reverse()
            create_new = cls(target)
        elif replace_with:
            old_obj = cls._get_object_from_version(operations, replace_with)
            drop_old = cls(target).reverse()
            create_new = cls(old_obj)
        else:
            raise TypeError("replaces or replace_with is required")

        operations.invoke(drop_old)
        operations.invoke(create_new)


@Operations.register_operation("create_fn", "invoke_for_target")
@Operations.register_operation("replace_fn", "replace")
class CreateFunctionOperation(ReversibleOperation):
    def reverse(self):
        return DropFunctionOperation(self.target)


@Operations.register_operation("drop_fn", "invoke_for_target")
class DropFunctionOperation(ReversibleOperation):
    def reverse(self):
        return CreateFunctionOperation(self.target)


@Operations.register_operation("create_trg", "invoke_for_target")
@Operations.register_operation("replace_trg", "replace")
class CreateTriggerOperation(ReversibleOperation):
    def reverse(self):
        return DropTriggerOperation(self.target)


@Operations.register_operation("drop_trg", "invoke_for_target")
class DropTriggerOperation(ReversibleOperation):
    def reverse(self):
        return CreateTriggerOperation(self.target)


@Operations.register_operation("create_vw", "invoke_for_target")
@Operations.register_operation("replace_vw", "replace")
class CreateViewOperation(ReversibleOperation):
    def reverse(self):
        return DropViewOperation(self.target)


@Operations.register_operation("drop_vw", "invoke_for_target")
class DropViewOperation(ReversibleOperation):
    def reverse(self):
        return CreateViewOperation(self.target)


@Operations.implementation_for(CreateFunctionOperation)
def create_fn(operations, operation):
    operations.execute(
        "CREATE FUNCTION %s %s"
        % (
            operation.target.name,
            operation.target.sql,
        )
    )


@Operations.implementation_for(DropFunctionOperation)
def drop_fn(operations, operation):
    operations.execute("DROP FUNCTION %s" % operation.target.name)


@Operations.implementation_for(CreateTriggerOperation)
def create_trg(operations, operation):
    operations.execute(
        "CREATE TRIGGER %s %s ON %s %s"
        % (
            operation.target.name,
            operation.target.when,
            operation.target.on,
            operation.target.sql,
        )
    )


@Operations.implementation_for(DropTriggerOperation)
def drop_trg(operations, operation):
    operations.execute(
        "DROP TRIGGER %s ON %s"
        % (
            operation.target.name,
            operation.target.on,
        )
    )


@Operations.implementation_for(CreateViewOperation)
def create_vw(operations, operation):
    operations.execute(
        "CREATE VIEW %s AS %s"
        % (
            operation.target.name,
            operation.target.sql,
        )
    )


@Operations.implementation_for(DropViewOperation)
def drop_vw(operations, operation):
    operations.execute("DROP VIEW %s" % operation.target.name)
