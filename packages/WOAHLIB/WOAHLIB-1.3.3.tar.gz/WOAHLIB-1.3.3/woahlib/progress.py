
def simple_progress_bar(total,it, prefix='', length=40):
    percent = ("{0:.1f}").format(100 * (it / float(total)))
    filled_length = int(length * it // total)
    bar = f"{'#' * filled_length}{'-' * (length - filled_length)}"
    print(f'\r{prefix} |{bar}| {percent}% Complete', end='\r')

if __name__ == "__main__":
    simple_progress_bar(50,1, prefix='test', length=30)

#hehe