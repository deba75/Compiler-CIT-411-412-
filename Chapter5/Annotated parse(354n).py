class Node:
    """
    পার্স ট্রি-এর একটি নোড।
    এটিতে গ্রামার সিম্বল (type), চাইল্ড নোড (children),
    এবং অ্যাট্রিবিউট (val বা lexval) থাকে।
    """
    def __init__(self, type, children=None, lexval=None):
        self.type = type
        self.children = children if children else []
        self.lexval = lexval  # 'digit' টার্মিনালের জন্য
        self.val = None       # সিনথেসাইজড অ্যাট্রিবিউট 'val'

    def __repr__(self):
        # এটি শুধু ডিবাগিং-এর জন্য।
        if self.val is not None:
            return f"Node({self.type}, val={self.val})"
        if self.lexval is not None:
            return f"Node({self.type}, lexval={self.lexval})"
        return f"Node({self.type})"

# --- ধাপ ১: "3 * 5 + 4 n" এর জন্য পার্স ট্রি-টি ম্যানুয়ালি তৈরি করা ---
# (এটি আগের মতোই আছে)
digit3 = Node('digit', lexval=3)
digit5 = Node('digit', lexval=5)
digit4 = Node('digit', lexval=4)

f3 = Node('F', children=[digit3])
t3 = Node('T', children=[f3])       
f5 = Node('F', children=[digit5])
t15 = Node('T', children=[t3, '*', f5]) 
e15 = Node('E', children=[t15])     
f4 = Node('F', children=[digit4])
t4 = Node('T', children=[f4])       
e19 = Node('E', children=[e15, '+', t4]) 
root = Node('L', children=[e19, 'n'])   

# --- ধাপ ২: পোস্ট-অর্ডার ট্রাভার্সাল দিয়ে অ্যাট্রিবিউট গণনা করা ---
# (এটি আগের মতোই আছে)
def compute_annotations(node):
    """
    ট্রি-এর প্রতিটি নোডে সিনথেসাইজড অ্যাট্রিবিউট 'val' গণনা করে।
    এটি একটি পোস্ট-অর্ডার ট্রাভার্সাল (প্রথমে চাইল্ড, তারপর প্যারেন্ট)।
    """
    for child in node.children:
        if isinstance(child, Node):
            compute_annotations(child)

    if node.type == 'F' and node.children[0].type == 'digit':
        node.val = node.children[0].lexval  # F.val = digit.lexval
    elif node.type == 'T' and len(node.children) == 1 and node.children[0].type == 'F':
        node.val = node.children[0].val     # T.val = F.val
    elif node.type == 'T' and len(node.children) == 3 and node.children[1] == '*':
        t1 = node.children[0]
        f = node.children[2]
        node.val = t1.val * f.val           # T.val = T1.val * F.val
    elif node.type == 'E' and len(node.children) == 1 and node.children[0].type == 'T':
        node.val = node.children[0].val     # E.val = T.val
    elif node.type == 'E' and len(node.children) == 3 and node.children[1] == '+':
        e1 = node.children[0]
        t = node.children[2]
        node.val = e1.val + t.val           # E.val = E1.val + T.val
    elif node.type == 'L':
        node.val = node.children[0].val     # L.val = E.val
    elif node.type == 'digit':
        node.val = node.lexval

# --- ধাপ ৩: সুন্দর করে ট্রি প্রিন্ট করা (মডিফায়েড অংশ) ---

def print_tree_structure(node):
    """
    রুট নোড প্রিন্ট করে এবং ট্রি আঁকার জন্য রিকার্সিভ হেল্পার কল করে।
    """
    # অ্যাট্রিবিউট ফরম্যাট করার হেল্পার
    def get_attr(n):
        if n.val is not None: return f"(val = {n.val})"
        if n.lexval is not None: return f"(lexval = {n.lexval})"
        return ""

    # রুট নোড প্রিন্ট
    print(f"{node.type} {get_attr(node)}")
    
    # চাইল্ডদের জন্য রিকার্সিভ ফাংশন কল
    _print_children(node.children, "")

def _print_children(children_list, prefix):
    """
    চাইল্ড নোডদের রিকার্সিভলি প্রিন্ট করে, সঠিক কানেক্টর (├──, └──) সহ।
    """
    if not children_list:
        return
        
    last_child_index = len(children_list) - 1
    
    for i, child in enumerate(children_list):
        is_last = (i == last_child_index)
        
        # কানেক্টর এবং পরবর্তী প্রিফিক্স ঠিক করা
        connector = "└── " if is_last else "├── "
        child_prefix = "    " if is_last else "│   "

        if isinstance(child, Node):
            # অ্যাট্রিবিউট ফরম্যাট করার হেল্পার
            def get_attr(n):
                if n.val is not None: return f"(val = {n.val})"
                if n.lexval is not None: return f"(lexval = {n.lexval})"
                return ""
            
            # নোড প্রিন্ট
            print(f"{prefix}{connector}{child.type} {get_attr(child)}")
            # রিকার্সন
            _print_children(child.children, prefix + child_prefix)
        else:
            # '+' বা '*' এর মতো স্ট্রিং টার্মিনাল প্রিন্ট
            print(f"{prefix}{connector}'{child}'")


# --- ধাপ ৪: গণনা চালানো এবং ফলাফল প্রিন্ট করা ---

# প্রথমে গণনা করুন
compute_annotations(root)

print("\n--- অ্যানোটেশন গণনার পরে (Annotated Parse Tree) ---")
# নতুন প্রিন্ট ফাংশন কল করুন
print_tree_structure(root)

print("\n-------------------------------------------")
print(f"চূড়ান্ত ফলাফল (Final Result): L.val = {root.val}")
print("-------------------------------------------")