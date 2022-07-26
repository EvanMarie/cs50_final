"""empty message

Revision ID: 25554dcc24f4
Revises: 
Create Date: 2022-07-26 19:29:58.784850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25554dcc24f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('permissions', sa.UnicodeText(), nullable=True),
    sa.Column('update_datetime', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('school_day',
    sa.Column('day_number', sa.Integer(), nullable=False),
    sa.Column('calendar_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('day_number')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('fs_uniquifier', sa.String(length=64), nullable=False),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_ip', sa.String(length=64), nullable=True),
    sa.Column('current_login_ip', sa.String(length=64), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.Column('tf_primary_method', sa.String(length=64), nullable=True),
    sa.Column('tf_totp_secret', sa.String(length=255), nullable=True),
    sa.Column('tf_phone_number', sa.String(length=128), nullable=True),
    sa.Column('create_datetime', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('update_datetime', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('us_totp_secrets', sa.Text(), nullable=True),
    sa.Column('us_phone_number', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('fs_uniquifier'),
    sa.UniqueConstraint('username')
    )
    op.create_table('app_state',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('current_day', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['current_day'], ['school_day.day_number'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=32), nullable=True),
    sa.Column('last_name', sa.String(length=32), nullable=True),
    sa.Column('note', sa.String(length=2048), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_first_name'), 'student', ['first_name'], unique=False)
    op.create_index(op.f('ix_student_last_name'), 'student', ['last_name'], unique=False)
    op.create_index(op.f('ix_student_note'), 'student', ['note'], unique=False)
    op.create_table('assignment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('school_day', sa.Integer(), nullable=True),
    sa.Column('student', sa.Integer(), nullable=True),
    sa.Column('subject', sa.String(length=64), nullable=True),
    sa.Column('content', sa.String(length=256), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('assigned_by', sa.Integer(), nullable=True),
    sa.Column('note', sa.String(length=2048), nullable=True),
    sa.ForeignKeyConstraint(['assigned_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['school_day'], ['school_day.day_number'], ),
    sa.ForeignKeyConstraint(['student'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assignment_content'), 'assignment', ['content'], unique=False)
    op.create_index(op.f('ix_assignment_note'), 'assignment', ['note'], unique=False)
    op.create_index(op.f('ix_assignment_subject'), 'assignment', ['subject'], unique=False)
    op.create_table('link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student', sa.Integer(), nullable=True),
    sa.Column('link', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['student'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('upcoming',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('day', sa.Integer(), nullable=True),
    sa.Column('student', sa.Integer(), nullable=True),
    sa.Column('content', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['day'], ['school_day.day_number'], ),
    sa.ForeignKeyConstraint(['student'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('note',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('school_day', sa.Integer(), nullable=True),
    sa.Column('assignment', sa.Integer(), nullable=True),
    sa.Column('student', sa.Integer(), nullable=True),
    sa.Column('content', sa.String(length=1024), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['assignment'], ['assignment.id'], ),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['school_day'], ['school_day.day_number'], ),
    sa.ForeignKeyConstraint(['student'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('note')
    op.drop_table('upcoming')
    op.drop_table('link')
    op.drop_index(op.f('ix_assignment_subject'), table_name='assignment')
    op.drop_index(op.f('ix_assignment_note'), table_name='assignment')
    op.drop_index(op.f('ix_assignment_content'), table_name='assignment')
    op.drop_table('assignment')
    op.drop_index(op.f('ix_student_note'), table_name='student')
    op.drop_index(op.f('ix_student_last_name'), table_name='student')
    op.drop_index(op.f('ix_student_first_name'), table_name='student')
    op.drop_table('student')
    op.drop_table('roles_users')
    op.drop_table('app_state')
    op.drop_table('user')
    op.drop_table('school_day')
    op.drop_table('role')
    # ### end Alembic commands ###
