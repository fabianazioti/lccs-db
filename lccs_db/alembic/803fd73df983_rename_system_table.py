"""rename_system_table.

Revision ID: 803fd73df983
Revises: 
Create Date: 2021-07-12 12:04:21.496603

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '803fd73df983'
down_revision = None
branch_labels = ('lccs_db',)
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # classification system table
    op.rename_table('class_systems', 'classification_systems', schema='lccs')
    op.create_index(op.f('idx_lccs_classification_systems_name'), 'classification_systems', ['name'], unique=False,
                    schema='lccs')
    op.drop_index('idx_lccs_class_systems_name', table_name='classification_systems', schema='lccs')
    op.drop_constraint(op.f('class_systems_name_key'), 'classification_systems', schema='lccs', type_='unique')
    op.create_unique_constraint(op.f('classification_systems_name_key'), 'classification_systems', ['name', 'version'],
                                schema='lccs')

    op.execute('ALTER SEQUENCE lccs.class_systems_id_seq RENAME TO classification_systems_id_seq')
    op.execute('ALTER INDEX lccs.class_systems_pkey RENAME TO classification_systems_pkey')

    # classes table
    op.drop_constraint('classes_name_key', 'classes', schema='lccs', type_='unique')
    op.alter_column('classes', 'class_system_id', new_column_name='classification_system_id', schema='lccs')
    op.create_unique_constraint(op.f('classes_name_key'), 'classes', ['name', 'classification_system_id'], schema='lccs')
    op.drop_index('idx_lccs_classes_class_system_id', table_name='classes', schema='lccs')
    op.create_index(op.f('idx_lccs_classes_classification_system_id'), 'classes', ['classification_system_id'], unique=False, schema='lccs')
    op.drop_constraint('classes_class_system_id_class_systems_fkey', 'classes', schema='lccs', type_='foreignkey')
    op.create_foreign_key(op.f('classes_classification_system_id_classification_systems_fkey'), 'classes', 'classification_systems', ['classification_system_id'], ['id'], source_schema='lccs', referent_schema='lccs', onupdate='CASCADE', ondelete='CASCADE')

    # style table
    op.drop_index('idx_lccs_styles_class_system_id', table_name='styles', schema='lccs')
    op.alter_column('styles', 'class_system_id', new_column_name='classification_system_id',
                    schema='lccs')
    op.create_index(op.f('idx_lccs_styles_classification_system_id'), 'styles', ['classification_system_id'], unique=False, schema='lccs')
    op.drop_constraint('styles_class_system_id_class_systems_fkey', 'styles', schema='lccs', type_='foreignkey')
    op.create_foreign_key(op.f('styles_classification_system_id_classification_systems_fkey'), 'styles', 'classification_systems', ['classification_system_id'], ['id'], source_schema='lccs', referent_schema='lccs', onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # classification systems
    op.rename_table('classification_systems', 'class_systems', schema='lccs')
    op.create_index(op.f('idx_lccs_class_systems_name'), 'class_systems', ['name'], unique=False,
                    schema='lccs')
    op.drop_index('idx_lccs_classification_systems_name', table_name='class_systems', schema='lccs')
    op.drop_constraint(op.f('classification_systems_name_key'), 'class_systems', schema='lccs', type_='unique')
    op.create_unique_constraint('name', 'version', name=op.f('class_systems_name_key'),
                                table_name='class_systems', schema='lccs')
    op.execute('ALTER SEQUENCE lccs.classification_systems_id_seq RENAME TO class_systems_id_seq')
    op.execute('ALTER INDEX lccs.classification_systems_pkey RENAME TO class_systems_pkey')

    # styles table
    op.alter_column('styles', 'classification_system_id', nullable=True, new_column_name='class_system_id',
                    schema='lccs')
    op.drop_constraint(op.f('styles_classification_system_id_classification_systems_fkey'), 'styles', schema='lccs', type_='foreignkey')
    op.create_foreign_key('styles_class_system_id_class_systems_fkey', 'styles', 'class_systems', ['class_system_id'], ['id'], source_schema='lccs', referent_schema='lccs', onupdate='CASCADE', ondelete='CASCADE')
    op.drop_index(op.f('idx_lccs_styles_classification_system_id'), table_name='styles', schema='lccs')
    op.create_index('idx_lccs_styles_class_system_id', 'styles', ['class_system_id'], unique=False, schema='lccs')

    # classes table
    op.alter_column('classes', 'classification_system_id', nullable=True, new_column_name='class_system_id',
                    schema='lccs')
    op.drop_constraint(op.f('classes_classification_system_id_classification_systems_fkey'), 'classes', schema='lccs', type_='foreignkey')
    op.create_foreign_key('classes_class_system_id_class_systems_fkey', 'classes', 'class_systems', ['class_system_id'], ['id'], source_schema='lccs', referent_schema='lccs', onupdate='CASCADE', ondelete='CASCADE')
    op.drop_index(op.f('idx_lccs_classes_classification_system_id'), table_name='classes', schema='lccs')
    op.drop_constraint(op.f('classes_name_key'), 'classes', schema='lccs', type_='unique')
    op.create_unique_constraint('classes_name_key', 'classes', ['name', 'class_system_id'], schema='lccs')
    op.create_index('idx_lccs_classes_class_system_id', 'classes', ['class_system_id'], unique=False, schema='lccs')
    # ### end Alembic commands ###
